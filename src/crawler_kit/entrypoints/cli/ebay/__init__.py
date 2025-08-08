from typer import Typer
from crawler_kit.modules.ebay.presentation.cli.handlers.handle_web import (
    crawl_web,
)

crawlers = Typer(name="ebay", help="Ebay crawler")
crawlers.command(name="web", help="Crawl Ebay web content by url")(crawl_web)
