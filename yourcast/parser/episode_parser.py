from pydantic import BaseModel
from yourcast.scraper.crawler import Sentence
from yourcast.scraper.run_scrape import EpisodeScrapeResult
from yourcast.tools.llm_helpers import get_llm_completion, OpenaiModelNames, get_llm_structured_response, LLMResponse
from yourcast.tools.helpers import load_json, store_json
from typing import List
import os
import json


class BulletPoint(BaseModel):
    bullet_point: str
    timestamp: int

class BulletPoints(BaseModel):
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
2. Keep the original timestamp from the main point.
3. Maintain all key information while being as concise and engaging as possible.
4. Write in a style that maximizes curiosity and interest—make each message so intriguing that a reader wants to listen to the podcast to learn more.
5. Remove any bullet point formatting or indentation.
6. Ensure each message is self-contained, informative, and irresistible to click.
7. Process ALL bullet points from the input—do not skip any.
8. Remove timestamp from the bulletpoint text
9. Each bulletpoint text should be no longer than 140 characters 

Format each output as a message with its timestamp, removing any bullet points or indentation while preserving all key information in a concise, engaging format. Return a complete list of all processed bullet points.
"""


class EpisodeParser:
    def __init__(self):
        pass 

    def parse(self, scraped_episode_file: EpisodeScrapeResult):
        transcript = self.concatenate_sentences(scraped_episode_file.sentences)
        user_prompt = f"""
        Here is the podcast transcript. Please extract the key takeaways following the format specified in the system prompt.

        Transcript:
        {transcript}

        Please provide a comprehensive summary with bullet points that capture the most important insights and information from the transcript.
        """
        free_form_response = get_llm_completion(raw_parser_system_prompt, user_prompt, MODEL)
        structured_response = get_llm_structured_response(structured_parser_system_prompt, free_form_response.content, BulletPoints, MODEL)
        parsed_bulletpoints = BulletPoints(**json.loads(structured_response.content))
        store_json(parsed_bulletpoints.model_dump(), "example_bulletpoints")
        return structured_response.content

    def concatenate_sentences(self, sentences: list[Sentence]):
        full_episode_text = ""
        for sentence in sentences:
            full_episode_text += sentence.text + f" ({sentence.start_time} sec) "
        return full_episode_text

if __name__ == "__main__":
    scraped_episodes_files = os.listdir("yourcast/assets/scrape_results/")
    for scraped_episode_file in scraped_episodes_files:
        scraped_episode = EpisodeScrapeResult(**load_json(f"yourcast/assets/scrape_results/{scraped_episode_file}"))
        parser = EpisodeParser()
        print(parser.parse(scraped_episode))
