from typer import Typer
from crawler_kit.modules.pchome.presentation.cli.handlers.handle_web import (
    crawl_web,
)

crawlers = Typer(name="pchome", help="Pchome crawler")
crawlers.command(name="web", help="crawl Pchome web content by url")(crawl_web)
