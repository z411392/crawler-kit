from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.entrypoints.cli.pchome import crawlers as pchome_crawlers
from crawler_kit.entrypoints.cli.ebay import crawlers as ebay_crawlers
from crawler_kit.entrypoints.cli.lazada import crawlers as lazada_crawlers
from crawler_kit.entrypoints.cli.amazon import crawlers as amazon_crawlers


def middleware(context: Context):
    loop = ensure_event_loop()  # noqa: F841
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


typer = Typer(callback=middleware)
typer.add_typer(pchome_crawlers)
typer.add_typer(ebay_crawlers)
typer.add_typer(lazada_crawlers)
typer.add_typer(amazon_crawlers)
