from click.core import Context


def handle_message(context: Context, url: str):
    print("url: " + url)
