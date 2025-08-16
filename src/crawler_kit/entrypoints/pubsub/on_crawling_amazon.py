from firebase_functions.pubsub_fn import (
    on_message_published,
    CloudEvent,
    MessagePublishedData,
)
from crawler_kit.utils.google_cloud.run_job import run_job
from crawler_kit.modules.general.enums.topic import Topic


@on_message_published(topic=str(Topic.Amazon))
def handle_crawl_amazon(
    task: CloudEvent[MessagePublishedData],
):
    run_job("amazon", "web", task.data.message.json["url"])
