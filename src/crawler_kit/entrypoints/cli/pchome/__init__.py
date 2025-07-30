from typer import Typer
from crawler_kit.modules.pchome.presentation.cli.handlers.handle_pchome import (
    handle_pchome,
)
from crawler_kit.modules.pchome.presentation.cli.handlers.handle_message import (
    handle_message,
)

crawlers = Typer(name="crawlers")
crawlers.command(name="pchome")(handle_pchome)
crawlers.command(name="message")(handle_message)