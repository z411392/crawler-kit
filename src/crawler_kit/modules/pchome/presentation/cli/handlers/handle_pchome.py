from click.core import Context
from crawler_kit.utils.google_cloud.publish_message import publish_message
from crawler_kit.modules.general.enums.topic import Topic


def handle_pchome(context: Context, url: str):
    topic = Topic.Pchome
    payload = dict(url=url)
    print(publish_message(topic, payload))