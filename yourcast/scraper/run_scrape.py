from datetime import datetime

from pydantic import BaseModel
from slugify import slugify

from yourcast.scraper.crawler import Crawler, Sentence
from yourcast.tools.helpers import load_json, setup_logger, store_json

logger = setup_logger(__name__, f"yourcast/assets/logs/scraper_logs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")


class EpisodeScrapeInput(BaseModel):
    episode_name: str
    podcast_name: str
    publication_date: str
    url: str


class EpisodeScrapeResult(BaseModel):
    episode_name: str
    podcast_name: str
    publication_date: str
    url: str
    sentences: list[Sentence]


def run_scraper():
    raw_episode_inputs = load_json("yourcast/assets/episode_urls.json")
    crawler = Crawler(is_headless=False, is_stealth=True)
    for idx, raw_episode_input in enumerate(raw_episode_inputs["raw_episodes"]):
        try:
            episode_scrape_input = EpisodeScrapeInput(**raw_episode_input)
            logger.info(
                f"Scraping episode {idx} of {len(raw_episode_inputs['raw_episodes'])}: "
                f"\n URL: {episode_scrape_input.url}, "
                f"\n Episode Name: {episode_scrape_input.episode_name}, "
                f"\n Podcast Name: {episode_scrape_input.podcast_name}"
            )
            sentences = crawler.crawl(episode_scrape_input.url)
            episode_scrape_result = EpisodeScrapeResult(
                episode_name=episode_scrape_input.episode_name,
                podcast_name=episode_scrape_input.podcast_name,
                publication_date=episode_scrape_input.publication_date,
                url=episode_scrape_input.url,
                sentences=sentences,
            )
            store_json(episode_scrape_result.model_dump(), f"yourcast/assets/scrape_results/{slugify(episode_scrape_input.episode_name)}.json")
        except Exception as e:
            logger.error(f"Error scraping episode {idx} of {len(raw_episode_inputs['raw_episodes'])}: {e}")
            continue


if __name__ == "__main__":
    run_scraper()
