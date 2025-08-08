from typer import Typer
from crawler_kit.modules.lazada.presentation.cli.handlers.handle_web import (
    crawl_web,
)

crawlers = Typer(name="lazada", help="Lazada crawler")
crawlers.command(name="web", help="Crawl Lazada web content by url")(crawl_web)
