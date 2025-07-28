from typer import Typer
from click.core import Context
from crawler_kit.entrypoints.utils.asyncio import ensure_event_loop
from crawler_kit.entrypoints.cli.greet import greet
from crawler_kit.entrypoints.cli.crawler import crawler


def callback(context: Context):
    loop = ensure_event_loop()
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


app = Typer(callback=callback)
app.add_typer(greet)
app.add_typer(crawler)
