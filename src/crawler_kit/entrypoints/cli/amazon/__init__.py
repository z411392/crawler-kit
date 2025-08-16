from typer import Typer
from crawler_kit.modules.amazon.presentation.cli.handlers.handle_crawl_amazon_web import (
    handle_crawl_amazon_web,
)

crawlers = Typer(name="amazon", help="Amazon crawler")
crawlers.command(name="web", help="Crawl Amazon web content by url")(
    handle_crawl_amazon_web
)
