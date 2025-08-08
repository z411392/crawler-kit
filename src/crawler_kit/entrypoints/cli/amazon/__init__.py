from typer import Typer
from crawler_kit.modules.amazon.presentation.cli.handlers.handle_web import (
    crawl_web,
)

crawlers = Typer(name="amazon", help="Amazon crawler")
crawlers.command(name="web", help="Crawl Amazon web content by url")(crawl_web)
