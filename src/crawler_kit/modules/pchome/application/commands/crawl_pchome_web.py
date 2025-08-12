from crawler_kit.modules.pchome.application.commands.pchome_crawler import PchomeCrawler
from crawler_kit.modules.pchome.application.commands.pchome_parser import PchomeParser
from crawler_kit.modules.pchome.application.commands.pchome_storage_service import (
    PchomeStorageService,
)
from prefect import flow, task, get_run_logger

class crawl_pchome_web:
    def __init__(self, request_delay: int, trace_id: str):
        self.crawler = PchomeCrawler(request_delay)
        self.parser = PchomeParser()
        self.storage = PchomeStorageService()
        self.trace_id = trace_id

    @flow
    def crawl(self, url: str, skip_if_exists: bool = False, parse_content: bool = True):
        logger = get_run_logger()
        try:
            logger.info(f"Crawling content from URL: {url}")
            content = self.crawler.crawl_page(url)
            if not content:
                logger.error(f"Failed to crawl content from URL: {url}")
                return False

            if skip_if_exists and self.storage.check_url_exists(url):
                logger.info(f"Skipping already crawled content for URL: {url}")
                return True

            if parse_content:
                logger.info(f"Parsing content for URL: {url}")
                parsed_data = self.parser.parse_product_page(content, url)
                logger.info(f"Parsed data: {parsed_data}")
                if not parsed_data:
                    logger.warning(f"Failed to parse content from URL: {url}")
                    return False

            if not self.storage.save_crawled_data(
                self.trace_id, url, content, parsed_data
            ):
                logger.error(f"Failed to save data for URL: {url}")
                return False
            logger.info(f"Successfully processed URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            return False

    def __call__(self, url: str):
        flow = self.crawl.with_options(flow_run_name=self.trace_id)
        return flow(url)
