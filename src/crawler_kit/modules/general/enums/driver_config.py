from enum import Enum
from typing import Dict
from fake_useragent import UserAgent
from crawler_kit.utils.environments import headless_flag
from os import getenv
import tempfile
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] %(name)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_extension_path():
    current_file = os.path.abspath(__file__)
    crawler_kit_dir = current_file
    for _ in range(4):  # modules -> general -> enums -> driver_config.py
        crawler_kit_dir = os.path.dirname(crawler_kit_dir)

    extension_path = os.path.join(
        crawler_kit_dir,
        "infrastructure",
        "plugins",
        "chrome",
        "CapSolver.Browser.Extension-v1.16",
    )

    if os.path.exists(extension_path):
        return os.path.abspath(extension_path)


headless = True if getenv("HEADLESS", "") == "True" else False


class DriverConfig(Dict, Enum):
    Ebay = {
        "browser": "chrome",
        "headless": headless,
        "proxy": None,
        "window_size": "1920,1080",
    }

    Amazon = {
        "browser": "chrome",
        "headless": headless,
        "proxy": None,
        "window_size": "1920,1080",
    }

    Lazada = {
        "browser": "chrome",
        "headless": headless,
        "proxy": None,
        "window_size": "1920,1080",
        # "chromium_arg": f"ignore-certificate-errors-spki-list,enable-features=AllowCrossOriginAuth,--user-data-dir={tempfile.mkdtemp()}",
        "page_load_strategy": "eager",
        "extension_dir": get_extension_path(),
        "locale_code": "en-US",
    }
