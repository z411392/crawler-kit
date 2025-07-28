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
    from firebase_functions.https_fn import on_request
    from crawler_kit.utils.asyncio import ensure_event_loop
    from crawler_kit.entrypoints.http.handle_admin_bff_request import (
        vellox as admin_bff,
    )

    @on_request()
    def handle_admin_bff_request(request):
        return ensure_event_loop().run_until_complete(admin_bff(request))
