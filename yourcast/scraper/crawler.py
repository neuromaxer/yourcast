import logging
import re
from typing import List

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from pydantic import BaseModel

from yourcast.tools.keywords import StaticNames

logger = logging.getLogger(StaticNames.scraper_logger_name)


class ScrapeResultMetadata(BaseModel):
    url: str
    title: str


class Sentence(BaseModel):
    text: str
    start_time: float
    speaker_id: int


def extract_links(markdown: str) -> dict:
    pattern = re.compile(r"\[([^\[\]]+?)\s*-+\s*([A-Za-z]{3,} \d{2}, \d{4})(\d+)\s+transcripts\]\((/pod/[^)]+)\)")
    matches = pattern.findall(markdown)
    podcast_info = {}
    for name_with_meta, date, transcript_count, url in matches:
        name = name_with_meta.strip()
        if int(transcript_count) > 0:
            podcast_info[name] = {
                "url": "https://www.readablepod.com" + url,
                "n_transcripts": int(transcript_count),
            }

    return podcast_info


class Crawler:
    def __init__(
        self,
        is_headless: bool = True,
        wait_until: str = "networkidle",
        is_stealth: bool = False,
    ):
        logger.info("Initializing Crawler")
        self.playwright = sync_playwright().start()
        self.is_headless = is_headless
        self.wait_until = wait_until
        self.browser = self.playwright.chromium.launch(headless=self.is_headless)
        self.page = self.get_new_page()
        self.urls_processed = 0
        self.max_urls_before_restart = 200
        self.is_stealth = is_stealth

    def crawl(self, url: str) -> List[Sentence]:
        logger.debug("Crawling...")

        if self.is_stealth:
            stealth_sync(self.page)
        self.page.goto(url, wait_until=self.wait_until, referer="https://google.com")

        # Extract sentences with timestamps and speaker info
        sentences = []

        # First find the article element
        article = self.page.query_selector("article")
        if not article:
            logger.warning("No article element found on the page")

        # Find speaker divs only within the article
        speaker_divs = article.query_selector_all('div[class*="prose mb-6 border-l-8"]')

        for speaker_idx, speaker_div in enumerate(speaker_divs):
            # Get all paragraphs within the speaker's div
            paragraphs = speaker_div.query_selector_all('p[class*="caption"]')

            for p in paragraphs:
                # Extract timestamp from id attribute
                id_attr = p.get_attribute("id")
                if id_attr and id_attr.startswith("start-"):
                    timestamp_str = id_attr.split("-")[1].split(" ")[0]
                    try:
                        # Convert timestamp to seconds (e.g., "17.4" -> 17.4)
                        timestamp = float(timestamp_str)
                    except ValueError:
                        continue

                    # Get the text content
                    text = p.text_content().strip()

                    if text:  # Only add non-empty sentences
                        sentences.append(Sentence(text=text, start_time=timestamp, speaker_id=speaker_idx))

        self.urls_processed += 1
        if self.urls_processed >= self.max_urls_before_restart:
            self.restart_browser()

        return sentences

    def get_new_page(self):
        context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        )
        return context.new_page()

    def restart_browser(self):
        logger.info("Restarting browser...")
        self.browser.close()
        self.browser = self.playwright.chromium.launch(headless=self.is_headless)
        self.page = self.get_new_page()
        self.urls_processed = 0

    def stop_playwright(self):
        self.browser.close()
        self.playwright.stop()
