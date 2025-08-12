import logging
import time
from typing import Optional
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
from crawler_kit.modules.general.enums.driver_config import DriverConfig


class EbayCrawler:
    def __init__(self, request_delay: int):
        self.browser_options = DriverConfig.Ebay.value
        self.request_delay = request_delay

    def crawl_page(self, url: str) -> Optional[str]:
        try:
            with SeleniumBaseManager.get_driver(**self.browser_options) as driver:
                driver.get(url)
                time.sleep(self.request_delay)

                content = driver.page_source
                return content
        except Exception as e:
            logging.error(f"Error crawling page {url}: {e}")
            return None
