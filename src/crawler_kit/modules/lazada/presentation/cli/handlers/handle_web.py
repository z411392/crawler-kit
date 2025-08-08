import logging
import hashlib
import time
import random
from click.core import Context
from crawler_kit.modules.general.enums.topic import Topic
from typing import Dict, Optional
from google.cloud import firestore
from crawler_kit.utils.google_cloud.credentials_from_env import (
    credentials_from_env,
)
from crawler_kit.infrastructure.webdriver.seleniumbase_manager import (
    SeleniumBaseManager,
)
import logging


logger = logging.getLogger(__name__)


class handle_lazada_web:
    def __init__(self, request_delay: int):
        self.browser_options = {
            "browser": "chrome",
            "headless": True,
            "window_size": "1920,1080",
        }

        self.request_delay = request_delay

        self.db = firestore.Client(credentials=credentials_from_env())
        self.source = "Lazada"
        self.type = "product"
        self.platform = "web"

    def _build_firestore_path(self) -> str:
        return f"sources/{self.source}/types/{self.type}/platforms/{self.platform}/raw"

    def _generate_content_hash(self, content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def _save_to_firestore(self, url: str, content: str) -> bool:
        try:
            content_hash = self._generate_content_hash(content)
            doc_data = {
                "url": url,
                "content": content,
                "crawledAt": firestore.SERVER_TIMESTAMP,
                "status": "success",
                "contentLen": len(content),
            }
            collection = self.db.collection(self._build_firestore_path())
            doc_ref = collection.document(content_hash)
            doc_ref.set(doc_data)
            return True
        except Exception as e:
            logger.error(f"Error saving to Firestore: {e}")
            return False

    def crawl(self, url: str):
        try:
            with SeleniumBaseManager.get_driver(**self.browser_options) as driver:
                driver.get(url)
                time.sleep(self.request_delay)

                content = driver.page_source
                if not self._save_to_firestore(url, content):
                    raise Exception("Failed to save to Firestore")
                return True
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            return False

    def __call__(self, context: Context, url: str):
        return self.crawl(url)


def crawl_web(url: str, request_delay: int = 1):
    handler = handle_lazada_web(request_delay)
    return handler.crawl(url)
