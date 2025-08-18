from crawler_kit.modules.lazada.application.commands.lazada_crawler import LazadaCrawler
from crawler_kit.modules.lazada.application.commands.lazada_parser import LazadaParser
from crawler_kit.modules.lazada.application.commands.lazada_storage_service import (
    LazadaStorageService,
)
from typing import NamedTuple, Optional, Dict
from prefect import flow, task, get_run_logger
from prefect.cache_policies import NO_CACHE


class CrawlerError(Exception):
    pass

class CrawlerResult(NamedTuple):
    url: str
    content: str
    parsed_data: Optional[Dict] = None


class LazadaWebCrawler:
    def __init__(self, request_delay: int, trace_id: str):
        self.crawler = LazadaCrawler(request_delay)
        self.parser = LazadaParser()
        self.storage = LazadaStorageService()
        self.trace_id = trace_id

    @flow(name="crawl-lazada-web")
    def __call__(
        self, url: str, skip_if_exists: bool = False, parse_content: bool = True
    ) -> bool:
        logger = get_run_logger()
        logger.info(f"Processing URL: {url}")
        try:
            if skip_if_exists and self.storage.check_url_exists(url):
                logger.info(f"Skipping already crawled content for URL: {url}")
                return True

            result = self._crawl_and_parse(url, parse_content)
            self._save_result(result)

            logger.info(f"Successfully processed URL: {url}")
            return True

        except CrawlerError as e:
            logger.error(f"Crawler error for URL {url}: {e}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error for URL {url}: {e}")
            return False

    @task(name="crawl-and-parse", cache_policy=NO_CACHE)
    def _crawl_and_parse(self, url: str, parse_content: bool = True) -> CrawlerResult:
        logger = get_run_logger()
        logger.info(f"Crawling content from: {url}")
        raw_content = self.crawler.crawl_page(url)
        if not raw_content:
            raise CrawlerError(f"Failed to crawl content from URL: {url}")

        parsed_data = None
        if parse_content:
            logger.info(f"Parsing content for: {url}")
            parsed_data = self.parser.parse_product_page(raw_content, url)
            if not parsed_data:
                raise CrawlerError("Failed to parse page content")

        return CrawlerResult(url=url, content=raw_content, parsed_data=parsed_data)

    @task(name="save-crawl-result", cache_policy=NO_CACHE)
    def _save_result(self, result: CrawlerResult):
        logger = get_run_logger()
        logger.info(f"Saving crawl result for URL: {result.url}")
        success = self.storage.save_crawled_data(
            self.trace_id,
            result.url,
            result.content,
            parsed_data=result.parsed_data,
        )

        if not success:
            raise CrawlerError(f"Failed to save crawl result for URL: {result.url}")
