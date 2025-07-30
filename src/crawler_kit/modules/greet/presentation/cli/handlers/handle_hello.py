from click.core import Context
from crawler_kit.utils.google_cloud.publish_message import publish_message
from crawler_kit.modules.general.enums.topic import Topic


def handle_hello(context: Context):
    topic = Topic.Test
    payload = dict(message="hello, world")
    print(publish_message(topic, payload))
