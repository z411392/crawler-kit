if __name__ == "__main__":
    from dotenv import load_dotenv
    from os.path import exists
    from os import environ
    from crawler_kit.entrypoints.cli import app

    environ["RUN_MODE"] = "cli"

    if exists("functions/.env"):
        load_dotenv("functions/.env", override=True)
    if exists("functions/.env.local"):
        load_dotenv("functions/.env.local", override=True)
    app()

else:
    from firebase_functions.https_fn import on_request
    from werkzeug.wrappers import Request
    from vellox import Vellox
    from crawler_kit.entrypoints.http.starlette import app
    from crawler_kit.utils.asyncio import ensure_event_loop

    vellox = Vellox(
        app=app,
    )

    @on_request()
    def handle_request(request: Request):
        loop = ensure_event_loop()
        return loop.run_until_complete(vellox(request))

    from firebase_functions.pubsub_fn import (
        on_message_published,
        CloudEvent,
        MessagePublishedData,
    )
    from os import getenv
    from crawler_kit.utils.google_cloud.run_job import run_job

    @on_message_published(topic=f"projects/{getenv('PROJECT_ID')}/topics/test")
    def on_test_message_received(
        event: CloudEvent[MessagePublishedData],
    ):
        run_job("greet", "world", event.data.message.json["message"])
