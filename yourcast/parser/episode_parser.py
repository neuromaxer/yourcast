import json
import logging
import os
import re
import time
from typing import List

import openai
from pinecone import Pinecone, ServerlessSpec
from pydantic import BaseModel
from tqdm import tqdm

from yourcast.scraper.crawler import Sentence
from yourcast.scraper.run_scrape import EpisodeScrapeResult
from yourcast.tools.helpers import load_json, make_id, store_json
from yourcast.tools.llm_helpers import OpenaiModelNames, get_llm_completion, get_llm_structured_response


class BulletPoint(BaseModel):
    text: str
    timestamp: int


class BulletPointMetadata(BaseModel):
    text: str
    timestamp: int
    episode_name: str
    source_podcast_name: str
    published_date: str
    listen_link: str
    image: str


class BulletPoints(BaseModel):
    episode_summary: str
    bullet_points: List[BulletPoint]


MODEL = OpenaiModelNames.gpt4o_mini

raw_parser_system_prompt = """
You are a world-class company providing podcast summaries and insights to help listeners save time by reading through the most important insights instead of listening to long podcasts.
You should support us in creating the articles we will send to our users. We will provide you with the podcast transcript.

Your task is to extract all the most engaging and informative takeaways from the podcast transcript. Be exhaustive: every topic and key point discussed in the podcast should be captured as a bullet point. Imagine each bullet point as a teaser tweet designed to spark curiosity and make the reader want to listen to the podcast for more.

For each takeaway:

1. Start with a clear, concise main idea that captures the key point and is phrased to intrigue and engage the reader.
2. Follow with specific examples or details mentioned in the transcript that add credibility and depth.
3. Include the timestamp (in seconds) from the first sentence that contributed to this takeaway.
4. Stay strictly true to the transcript—do not add information that wasn't explicitly mentioned.
5. Focus on actionable insights, surprising facts, or concrete information that would make someone want to learn more.
6. The header should be in consulting style, stating the core message of the topic in a way that grabs attention.

Format each takeaway as a bullet point with the main idea and timestamp, followed by indented supporting details. Group related points together and maintain a logical flow throughout the summary. Ensure that no important topic or point from the transcript is omitted, and that each bullet point is crafted to make the user want to click and listen to the podcast.
"""

structured_parser_system_prompt = """
You are a professional content editor specializing in creating concise, impactful, and highly engaging messages from longer content.

Your task is to transform bullet points with supporting details into clear, compelling message. For each bullet point:

1. Combine the main point and supporting details into a coherent message that can consist of multiple short, punchy sentences.
2. Maintain all key information while being as concise and engaging as possible.
3. Write in a style that maximizes curiosity and interest—make each message so intriguing that a reader wants to listen to the podcast to learn more.
4. Ensure each message is self-contained, informative, and irresistible to click.
5. Process ALL bullet points from the input—do not skip any.
9. Each bulletpoint text should be no longer than 140 characters
10. Also provide a summary of the episode in the episode_summary field which should be no longer than 280 characters

Format each output as a message with its timestamp, removing any bullet points or indentation while preserving all key information in a concise, engaging format. Return a complete list of all processed bullet points.
"""

episode_summaries = load_json("yourcast/assets/episode_summaries.json") if os.path.exists("yourcast/assets/episode_summaries.json") else {}
podcast_images = load_json("yourcast/assets/podcast_images.json")


class EpisodeParser:
    def __init__(self, pinecone_index=None):
        self.pinecone_index = pinecone_index

    def episode_already_upserted(self, source_podcast_name: str, published_date: str, episode_name: str) -> bool:
        """Check if an episode has already been upserted to Pinecone by metadata."""
        if not self.pinecone_index:
            raise ValueError("Pinecone index not initialized.")
        # Query Pinecone for a vector with matching metadata
        # We'll use a metadata filter for all three fields
        query_filter = {
            "source_podcast_name": source_podcast_name,
            "published_date": published_date,
            "episode_name": episode_name,
        }
        # Query with a dummy vector (all zeros) and top_k=1, using filter
        # (Assumes at least one vector per episode)
        try:
            response = self.pinecone_index.query(
                vector=[0.0] * 1536,
                top_k=1,
                filter=query_filter,
                include_metadata=False,
            )
            return len(response.matches) > 0
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return False

    def parse(self, scraped_episode_file: EpisodeScrapeResult):
        transcript = self.concatenate_sentences(scraped_episode_file.sentences)
        free_form_user_prompt = f"""
        Here is the podcast transcript. Please extract the key takeaways following the format specified in the system prompt.

        Transcript:
        {transcript}

        Please provide a comprehensive summary with bullet points that capture the most important insights and information from the transcript.
        """

        free_form_response = get_llm_completion(raw_parser_system_prompt, free_form_user_prompt, MODEL)

        structured_user_prompt = f"""
        Here is the free form summary of the episode.
        {free_form_response.content}

        Please transform the bullet points into a concise, engaging message and provide a summary of the episode in the episode_summary field
        """
        structured_response = get_llm_structured_response(structured_parser_system_prompt, structured_user_prompt, BulletPoints, MODEL)
        parsed_bulletpoints = BulletPoints(**json.loads(structured_response.content))
        episode_summaries[scraped_episode_file.episode_name] = parsed_bulletpoints.episode_summary
        store_json(episode_summaries, "yourcast/assets/episode_summaries.json")
        return parsed_bulletpoints

    def concatenate_sentences(self, sentences: list[Sentence]):
        full_episode_text = ""
        for sentence in sentences:
            full_episode_text += sentence.text + f" ({sentence.start_time} sec) "
        return full_episode_text

    def upsert_bulletpoints_batch(
        self,
        bulletpoints: list[BulletPoint],
        source_podcast_name: str,
        published_date: str,
        episode_name: str,
        listen_link: str = "",
        batch_size: int = 32,
    ):
        """Batch embed and upsert bullet points to Pinecone with metadata."""
        if not self.pinecone_index:
            raise ValueError("Pinecone index not initialized.")

        for i in range(0, len(bulletpoints), batch_size):
            batch = bulletpoints[i : i + batch_size]
            # Remove " (xxx sec)" from bullet point text using regex
            texts = [re.sub(r"\s*\(\d+\s*sec\)", "", bp.text) for bp in batch]
            # Batch embed
            response = openai.embeddings.create(input=texts, model="text-embedding-3-small")
            embeddings = [d.embedding for d in response.data]
            # Prepare upsert dicts
            upserts = []
            for idx, (bp, emb) in enumerate(zip(batch, embeddings)):
                upserts.append(
                    {
                        "id": make_id(bp.text, i + idx),
                        "values": emb,
                        "metadata": BulletPointMetadata(
                            text=bp.text,
                            timestamp=bp.timestamp,
                            episode_name=episode_name,
                            source_podcast_name=source_podcast_name,
                            published_date=published_date,
                            listen_link=listen_link,
                            image=podcast_images[source_podcast_name],
                        ).model_dump(),
                    }
                )
            # Upsert to Pinecone
            self.pinecone_index.upsert(upserts)
        print("Upsert complete.")


def initialise_pinecone_index(index_name):
    # configure client
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    cloud = os.environ.get("PINECONE_CLOUD") or "aws"
    region = os.environ.get("PINECONE_REGION") or "us-east-1"

    spec = ServerlessSpec(cloud=cloud, region=region)

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pc.list_indexes().names():
        # if does not exist, create index
        pc.create_index(index_name, dimension=1536, metric="cosine", spec=spec)
        # wait for index to be initialized
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    # connect to index
    index = pc.Index(index_name)
    return index


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    scraped_episodes_files = os.listdir("yourcast/assets/scrape_results/")
    index_name = "yourpod"
    index = initialise_pinecone_index(index_name)

    upserted_count = 0

    for scraped_episode_file in tqdm(scraped_episodes_files, desc="Upserting episodes", unit="episode"):
        scraped_episode = EpisodeScrapeResult(**load_json(f"yourcast/assets/scrape_results/{scraped_episode_file}"))
        parser = EpisodeParser(index)
        # Check if already upserted
        if parser.episode_already_upserted(
            scraped_episode.podcast_name,
            scraped_episode.publication_date,
            scraped_episode.episode_name,
        ):
            logging.info(
                f"Episode '{scraped_episode.episode_name}' from '{scraped_episode.podcast_name}' ({scraped_episode.publication_date}) already upserted. Skipping."
            )
            continue

        parsed_bulletpoints = parser.parse(scraped_episode)
        parser.upsert_bulletpoints_batch(
            parsed_bulletpoints.bullet_points,
            scraped_episode.podcast_name,
            scraped_episode.publication_date,
            scraped_episode.episode_name,
        )
        upserted_count += 1
        logging.info(
            f"Parsed and upserted episode '{scraped_episode.episode_name}' from '{scraped_episode.podcast_name}' ({scraped_episode.publication_date}) to Pinecone. "
            f"Progress: {upserted_count}/{len(scraped_episodes_files)}"
        )
