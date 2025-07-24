from typer import Typer
from crawler_kit.modules.greet.presentation.cli.handlers.handle_hello import (
    handle_hello,
)

greet = Typer(name="greet")
greet.command(name="hello")(handle_hello)
