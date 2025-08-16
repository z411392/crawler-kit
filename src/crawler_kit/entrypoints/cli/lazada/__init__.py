from typer import Typer
from crawler_kit.modules.lazada.presentation.cli.handlers.handle_crawl_lazada_web import (
    handle_crawl_lazada_web,
)

crawlers = Typer(name="lazada", help="Lazada crawler")
crawlers.command(name="web", help="Crawl Lazada web content by url")(
    handle_crawl_lazada_web
)
