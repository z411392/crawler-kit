from typer import Typer
from crawler_kit.entrypoints.cli.greet.handle_hello import handle_hello
from crawler_kit.entrypoints.cli.greet.handle_world import handle_world

greet = Typer(name="greet")
greet.command(name="hello")(handle_hello)
greet.command(name="world")(handle_world)
