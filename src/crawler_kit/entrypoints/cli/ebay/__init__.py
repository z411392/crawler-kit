from typer import Typer
from crawler_kit.modules.ebay.presentation.cli.handlers.handle_crawl_ebay_web import (
    handle_crawl_ebay_web,
)

crawlers = Typer(name="ebay", help="Ebay crawler")
crawlers.command(name="web", help="Crawl Ebay web content by url")(
    handle_crawl_ebay_web
)
