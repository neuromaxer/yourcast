from yourcast.scraper.crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler(is_headless=False, is_stealth=True)
    crawler.crawl("https://www.readablepod.com/pod")
