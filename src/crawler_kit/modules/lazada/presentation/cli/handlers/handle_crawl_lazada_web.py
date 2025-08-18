from crawler_kit.modules.lazada.application.commands.crawl_lazada_web import (
    LazadaWebCrawler,
)
from shortuuid import uuid
from os import environ


def handle_crawl_lazada_web(url: str, request_delay: int = 15, dev: bool = False):
    trace_id = uuid()
    if not dev:
        environ.setdefault("HEADLESS", "True")
    handler = LazadaWebCrawler(request_delay, trace_id)
    flow = handler.__call__.with_options(flow_run_name=trace_id)
    return flow(url)
