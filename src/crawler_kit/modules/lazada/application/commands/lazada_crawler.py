import time
import random
from typing import Optional
from selenium.webdriver.common.by import By
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
from crawler_kit.modules.general.enums.driver_config import DriverConfig
from prefect.cache_policies import NO_CACHE
from prefect import flow, get_run_logger, task


class CrawlerError(Exception):
    pass


class LazadaCrawler:
    def __init__(self, request_delay: int = 10):
        self.request_delay = request_delay

    @flow(name="crawl-lazada-page")
    def crawl_page(self, url: str) -> Optional[str]:
        logger = get_run_logger()
        logger.info(f"Start crawl page: {url}")
        try:
            content = self._fetch_page_content(url)
            logger.info(f"Successfully crawled page: {url}")
            return content
        except CrawlerError as e:
            logger.error(f"Crawler error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            return None

    @task(name="fetch-page-content", cache_policy=NO_CACHE)
    def _fetch_page_content(self, url: str) -> str:
        with self._get_driver() as driver:
            self._load_page(driver, url)
            self._wait_for_page_ready(driver)
            return driver.page_source

    @task(name="load-page", cache_policy=NO_CACHE)
    def _load_page(self, driver, url: str):
        logger = get_run_logger()
        logger.info(f"Start load page: {url}")
        driver.get(url)
        time.sleep(self.request_delay)

    @task(name="wait-for-page-ready", cache_policy=NO_CACHE)
    def _wait_for_page_ready(self, driver, timeout: int = 60, check_interval: int = 7):
        logger = get_run_logger()

        for attempt in range(1, timeout // check_interval + 1):
            logger.info(f"Check page status - attempt {attempt}")

            if not self._has_captcha(driver):
                logger.info("Page is ready, no CAPTCHA")
                return

            logger.warning(
                f"Detected CAPTCHA, waiting {check_interval} seconds before retry..."
            )
            time.sleep(check_interval)

        raise CrawlerError("Page failed to load within timeout")

    def _has_captcha(self, driver) -> bool:
        return (
            "punish?x5secdata=" in driver.current_url
            or len(driver.find_elements(By.TAG_NAME, "iframe")) >= 2
        )

    def _get_driver(self):
        return SeleniumBaseManager.get_driver(**DriverConfig.Lazada.value)


if __name__ == "__main__":
    LazadaCrawler(5).crawl_page(
        "https://www.lazada.co.th/products/proskin-capsule-12-i5134053435.html"
    )
