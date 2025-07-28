from google.cloud.pubsub import PublisherClient
from crawler_kit.utils.google_cloud.credentials_from_env import credentials_from_env
from json import dumps
from asyncio import Future
from google.api_core.exceptions import AlreadyExists
from os import getenv


def publish_message(topic: str, payload: dict):
    pubsub = PublisherClient(credentials=credentials_from_env())
    name = str(f"projects/{getenv('PROJECT_ID')}/topics/{topic}")
    try:
        pubsub.create_topic(
            request=dict(name=name),
        )
    except AlreadyExists:
        pass
    data = bytes(dumps(payload), "utf-8")
    future: Future = pubsub.publish(name, data)
    return future.result()
