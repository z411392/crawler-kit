from crawler_kit.modules.amazon.application.commands.crawl_amazon_web import (
    crawl_amazon_web,
)
from shortuuid import uuid


def handle_crawl_amazon_web(url: str, request_delay: int = 1):
    trace_id = uuid()
    handler = crawl_amazon_web(request_delay, trace_id)
    return handler(url)
