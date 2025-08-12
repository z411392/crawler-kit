from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from vellox import Vellox
from firebase_functions.https_fn import on_request
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.modules.general.presentation.http.handlers.handle_dispatch_crawling_job import (
    handle_dispatch_crawling_job,
)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

routes = [
    Route(
        "/sources/{source}/types/{type}/platforms/{platform}",
        handle_dispatch_crawling_job,
        methods=["POST"],
    ),
]

starlette = Starlette(
    middleware=middleware,
    lifespan=None,
    routes=routes,
    debug=False,
)

vellox = Vellox(
    app=starlette,
)


@on_request()
def admin(request):
    ensure_event_loop()
    return vellox(request)
