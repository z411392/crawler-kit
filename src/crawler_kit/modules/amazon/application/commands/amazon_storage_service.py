import logging
import hashlib
from typing import Dict, Optional
from google.cloud import firestore
from crawler_kit.utils.google_cloud.credentials_from_env import (
    credentials_from_env,
)
from crawler_kit.modules.general.enums.topic import Topic

logger = logging.getLogger(__name__)


class AmazonStorageService:
    def __init__(self):
        self.db = firestore.Client(credentials=credentials_from_env())
        topic = Topic.Amazon
        self.source = topic.value
        self.type = "product"
        self.platform = "web"

    def _build_firestore_path(self) -> str:
        return f"sources/{self.source}/types/{self.type}/platforms/{self.platform}/raw"

    def _generate_content_hash(self, content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def save_crawled_data(
        self, trace_id: str, url: str, content: str, parsed_data: Optional[Dict] = None
    ) -> bool:
        try:
            content_hash = self._generate_content_hash(content)
            doc_data = {
                "trace_id": trace_id,
                "url": url,
                "content": content[:10000],
                "crawledAt": firestore.SERVER_TIMESTAMP,
                "status": "success",
                "contentLen": len(content),
            }

            if parsed_data:
                doc_data["parsed"] = parsed_data
                doc_data["hasParsedData"] = True
            else:
                doc_data["hasParsedData"] = False

            collection = self.db.collection(self._build_firestore_path())
            doc_ref = collection.document(content_hash)
            doc_ref.set(doc_data)

            logger.info(f"Successfully saved data for URL: {url}")
            return True

        except Exception as e:
            logger.error(f"Error saving to Firestore: {e}")
            return False

    def check_url_exists(self, url: str) -> bool:
        try:
            collection = self.db.collection(self._build_firestore_path())
            docs = collection.where("url", "==", url).limit(1).get()

            exists = len(docs) > 0
            if exists:
                logger.info(f"URL already exists in Firestore: {url}")

            return exists

        except Exception as e:
            logger.error(f"Error checking URL existence: {e}")
            return False
