from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from typing import Optional, Generator
from contextlib import contextmanager
import logging
import time


logger = logging.getLogger(__name__)


class SeleniumBaseManager:
    @classmethod
    def create_driver(cls, browser, headless, **kwargs) -> Driver:
        driver_options = {"browser": browser, "headless": headless, **kwargs}

        start_time = time.time()
        try:
            driver = Driver(uc=True, **driver_options)

            startup_time = time.time() - start_time
            logger.info(f"WebDriver created successfully in {startup_time:.2f}s")

            return driver
        except Exception as e:
            logger.error(f"Error creating driver: {e}")
            raise

    @classmethod
    @contextmanager
    def get_driver(cls, browser, headless, **kwargs):
        driver = cls.create_driver(browser=browser, headless=headless, **kwargs)
        try:
            yield driver
        finally:
            if driver:
                driver.quit()


if __name__ == "__main__":
    with SeleniumBaseManager.get_driver(
        browser="chrome",
        headless=False,
        window_size="1920,1080",
    ) as driver:
        driver.get(
            "https://medium.com/@mkaanaslan99/time-series-forecasting-with-a-basic-transformer-model-in-pytorch-650f116a1018"
        )
        time.sleep(5)
