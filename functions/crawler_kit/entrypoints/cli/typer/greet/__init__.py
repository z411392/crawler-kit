from typer import Typer
from crawler_kit.modules.greet.presentation.cli.handlers.handle_hello import (
    handle_hello,
)
from crawler_kit.modules.greet.presentation.cli.handlers.handle_world import (
    handle_world,
)

greet = Typer(name="greet")
greet.command(name="hello")(handle_hello)
greet.command(name="world")(handle_world)
