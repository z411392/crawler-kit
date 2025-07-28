from click.core import Context
from crawler_kit.entrypoints.utils.google_cloud.publish_message import publish_message

def handle_crawl(context: Context, url:str, service:str):
    """
    發送爬蟲任務
    """
    topic = "crawl-tasks"
    payload = {"url": url, "service": service, "action": "crawl"}
    try:
        result= publish_message(topic, payload=payload)
        print(f"✅ 爬蟲任務已發送: {url}")
        return result
    except Exception as e:
        raise
    