from crawler_kit.modules.ebay.application.commands.crawl_ebay_web import EbayWebCrawler
from shortuuid import uuid
from os import environ

def handle_crawl_ebay_web(url: str, request_delay: int = 1, dev: bool = False):
    trace_id = uuid()
    if not dev:
        environ.setdefault("HEADLESS", "True")
    handler = EbayWebCrawler(request_delay, trace_id)
    flow = handler.__call__.with_options(flow_run_name=trace_id)
    return flow(url)
