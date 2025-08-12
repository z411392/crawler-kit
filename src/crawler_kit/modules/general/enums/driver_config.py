from enum import Enum
from typing import Dict
from fake_useragent import UserAgent

class DriverConfig(Dict, Enum):
    Ebay = {
        "browser": "chrome",
        "headless": False,
        "proxy": None,
        "window_size": "1920,1080",
    }

    Amazon = {
        "browser": "chrome",
        "headless": False,
        "proxy": None,
        "window_size": "1920,1080",
    }

    Lazada = {
        "browser": "chrome",
        "headless": False,
        "proxy": None,
        "window_size": "1920,1080",
        "chromium_arg": "ignore-certificate-errors-spki-list,enable-features=AllowCrossOriginAuth",
        "page_load_strategy": "eager",
        "extension_dir": "src/crawler_kit/infrastructure/plugins/chrome/CapSolver.Browser.Extension-v1.16"
    }
        