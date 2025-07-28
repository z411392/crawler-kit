from typer import Typer
from crawler_kit.entrypoints.cli.crawler.crawl import handle_crawl
# from crawler_kit.entrypoints.cli.crawler.process import handle_process

crawler = Typer(name="crawler")
crawler.command(name="crawl")(handle_crawl)
# crawler.command(name="process")(handle_process)
