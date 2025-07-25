from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.entrypoints.cli.typer.greet import greet


def callback(context: Context):
    loop = ensure_event_loop()
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


app = Typer(callback=callback)
app.add_typer(greet)
