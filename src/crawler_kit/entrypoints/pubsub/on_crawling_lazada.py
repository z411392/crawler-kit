from firebase_functions.pubsub_fn import (
    on_message_published,
    CloudEvent,
    MessagePublishedData,
)
from crawler_kit.utils.google_cloud.run_job import run_job
from crawler_kit.modules.general.enums.topic import Topic


@on_message_published(topic=str(Topic.Lazada))
def handle_crawl_lazada(
    task: CloudEvent[MessagePublishedData],
):
    run_job("lazada", "web", task.data.message.json["url"])
