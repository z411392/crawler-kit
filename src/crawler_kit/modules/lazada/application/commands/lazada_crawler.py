import time
import random
from typing import Optional
from selenium.webdriver.common.by import By
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
from crawler_kit.modules.general.enums.driver_config import DriverConfig

from prefect import flow, get_run_logger


class LazadaCrawler:
    def __init__(self, request_delay: int):
        self.browser_options = DriverConfig.Lazada.value
        self.request_delay = request_delay

    @flow
    def crawl_page(self, url: str) -> Optional[str]:
        try:
            logger = get_run_logger()
            with SeleniumBaseManager.get_driver(**self.browser_options) as driver:
                logger.info(f"start load page {url}")
                driver.get(url)
                self._smart_wait(driver, max_wait_time=50, check_interval=10)

                content = driver.page_source
                return content
        except Exception as e:
            logger.error(f"Error crawling page {url}: {e}")
            return None

    @flow
    def _check_for_recaptcha(self, driver) -> bool:
        try:
            logger = get_run_logger()
            logger.info("start check reCAPTCHA...")

            current_url = driver.current_url
            logger.info(f"current URL: {current_url[:100]}...")

            has_punish_url = "punish?x5secdata=" in current_url
            logger.info(f"URL contains punish?x5secdata=: {has_punish_url}")

            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            iframe_count = len(iframes)
            logger.info(f"found {iframe_count} iframe(s)")

            if has_punish_url:
                logger.info("❌ find reCAPTCHA (punish URL detected), wait longer...")
                return True
            elif iframe_count >= 2:
                logger.info(
                    "❌ find reCAPTCHA (multiple iframes detected), wait longer..."
                )
                return True
            else:
                logger.info("✅ no reCAPTCHA detected (normal page)")
                return False

        except Exception as e:
            logger.warning(f"error checking reCAPTCHA: {e}")
            return False

    @flow
    def _smart_wait(self, driver, max_wait_time: int = 50, check_interval: int = 10):
        logger = get_run_logger()
        time.sleep(self.request_delay)
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < max_wait_time:
            logger.info(
                f"⏰ Check #{int(elapsed_time / check_interval) + 1} (waited {elapsed_time:.0f}s)"
            )

            if self._check_for_recaptcha(driver):
                logger.info(
                    f"🎯 reCAPTCHA detected! Total wait time: {elapsed_time:.0f}s"
                )
                logger.info(f"💤 Waiting {check_interval}s before next check...")
                time.sleep(check_interval)
            else:
                logger.info("✅ no reCAPTCHA detected (normal page)")
                break
            elapsed_time = time.time() - start_time
        time.sleep(random.randint(3, 5))


if __name__ == "__main__":
    LazadaCrawler(5).crawl_page(
        "https://www.lazada.co.th/products/proskin-capsule-12-i5134053435.html"
    )
