from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.entrypoints.cli.greet import greet
from crawler_kit.entrypoints.cli.pchome import crawlers


def middleware(context: Context):
    loop = ensure_event_loop()  # noqa: F841
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


typer = Typer(callback=middleware)
typer.add_typer(greet)
typer.add_typer(crawlers)
