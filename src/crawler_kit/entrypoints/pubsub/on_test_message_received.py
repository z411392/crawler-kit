from firebase_functions.pubsub_fn import (
    on_message_published,
    CloudEvent,
    MessagePublishedData,
)
from crawler_kit.utils.google_cloud.run_job import run_job
from crawler_kit.modules.general.enums.topic import Topic


@on_message_published(topic=str(Topic.Test))
def handle_run_job_on_test_message_received(
    event: CloudEvent[MessagePublishedData],
):
    run_job("greet", "world", event.data.message.json["message"])
