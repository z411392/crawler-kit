from click.core import Context
from crawler_kit.utils.google_cloud.publish_message import publish_message


def handle_hello(context: Context):
    topic = "test"
    payload = dict(message="hello, world")
    print(publish_message(topic, payload))
