from google.cloud.pubsub import PublisherClient
from crawler_kit.utils.google_cloud.credentials_from_env import credentials_from_env
from json import dumps
from asyncio import Future
from google.api_core.exceptions import AlreadyExists
from crawler_kit.modules.general.enums.topic import Topic


def publish_message(topic: Topic, payload: dict):
    pubsub = PublisherClient(credentials=credentials_from_env())
    name = str(topic)
    try:
        pubsub.create_topic(
            request=dict(name=name),
        )
    except AlreadyExists:
        print(f"topic {name} already exists")
    data = bytes(dumps(payload), "utf-8")
    future: Future = pubsub.publish(name, data)
    return future.result()
