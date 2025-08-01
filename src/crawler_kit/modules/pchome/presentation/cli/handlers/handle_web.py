import logging
import hashlib
import httpx
import random
from click.core import Context
from crawler_kit.modules.general.enums.topic import Topic
from typing import Dict
from google.cloud import firestore
from crawler_kit.utils.google_cloud.credentials_from_env import (
    credentials_from_env,
)

logger = logging.getLogger(__name__)


class handle_pchome_web:
    def __init__(self, request_delay):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]

        self.client = httpx.Client(
            timeout=httpx.Timeout(30),
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )
        self.request_delay = request_delay
        self.db = firestore.Client(credentials=credentials_from_env())
        self.source = "PCHome"
        self.type = "product"
        self.platform = "web"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://24h.pchome.com.tw/",
            "Cache-Control": "no-cache",
        }

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

    def __call__(self, context: Context, url: str):
        try:
            topic = Topic.Pchome
            payload = dict(url=url)

            response = self.client.get(url, headers=self._get_headers())
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                )

            content = response.text

            success = self._save_to_firestore(url, content)
            if success:
                # 可選：發送成功訊息到 Pub/Sub
                # publish_message(topic, payload)
                logger.info(f"爬取完成: {url}")
            else:
                logger.error(f"爬取失敗: {url}")
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP 狀態錯誤 {e.response.status_code}: {url}"
            logger.error(error_msg)

        except httpx.RequestError as e:
            error_msg = f"請求錯誤: {str(e)} - URL: {url}"
            logger.error(error_msg)

        except Exception as e:
            logger.error(f"爬取過程發生錯誤: {e} - URL: {url}")

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()


def crawl_web(url: str, request_delay: int = 1):
    handler = handle_pchome_web(request_delay)
    handler(None, url)
