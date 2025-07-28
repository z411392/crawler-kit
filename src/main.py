if __name__ == "__main__":
    from dotenv import load_dotenv
    from os.path import exists
    from os import environ
    from crawler_kit.entrypoints.cli import typer

    environ["RUN_MODE"] = "cli"

    if exists("src/.env"):
        load_dotenv("src/.env", override=True)

    if exists("src/.env.local"):
        load_dotenv("src/.env.local", override=True)

    typer()

else:
    from crawler_kit.entrypoints.pubsub.on_test_message_received import *  # noqa: F403
    from crawler_kit.entrypoints.http.admin import admin  # noqa: F401
