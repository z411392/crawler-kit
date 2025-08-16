from crawler_kit.modules.lazada.application.commands.crawl_lazada_web import (
    crawl_lazada_web,
)
from shortuuid import uuid
from os import environ


def handle_crawl_lazada_web(url: str, request_delay: int = 15, dev: bool = False):
    trace_id = uuid()
    if not dev:
        environ.setdefault("HEADLESS", "True")
    handler = crawl_lazada_web(request_delay, trace_id)
    return handler(url)
