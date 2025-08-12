from crawler_kit.modules.ebay.application.commands.crawl_ebay_web import crawl_ebay_web
from shortuuid import uuid


def handle_crawl_ebay_web(url: str, request_delay: int = 1):
    trace_id = uuid()
    handler = crawl_ebay_web(request_delay, trace_id)
    return handler(url)
