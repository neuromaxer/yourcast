import logging
import re
import time

from markdownify import markdownify as md  # TODO: consider migrating to https://github.com/microsoft/markitdown
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from pydantic import BaseModel

from yourcast.tools.keywords import StaticNames

logger = logging.getLogger(StaticNames.scraper_logger_name)


class ScrapeResultMetadata(BaseModel):
    url: str
    title: str


class ScrapeResult(BaseModel):
    metadata: ScrapeResultMetadata
    markdown: str
    html: str


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
        wait_until: str = "load",
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

    def crawl(self, url: str) -> ScrapeResult:
        # TODO: Apply standard scraping logic to big aggregators like zalando, asos (already have those scripts)
        logger.debug("Crawling...")
        # check_if_valid_url(url)

        if self.is_stealth:
            stealth_sync(self.page)
        self.page.goto(url, wait_until=self.wait_until, referer="https://google.com")
        self.page.mouse.wheel(0, 100000)
        time.sleep(1)
        self.page.mouse.wheel(0, -100000)
        time.sleep(1)
        markdown = md(self.page.content()).replace("\n", "")

        scrape_result = ScrapeResult(
            metadata=ScrapeResultMetadata(url=url, title=self.page.title()),
            markdown=markdown,
            html=self.page.content(),
        )

        self.urls_processed += 1
        if self.urls_processed >= self.max_urls_before_restart:
            self.restart_browser()

        return scrape_result

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
