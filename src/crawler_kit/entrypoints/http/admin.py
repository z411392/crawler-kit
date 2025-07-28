from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from vellox import Vellox
from firebase_functions.https_fn import on_request
from crawler_kit.utils.asyncio import ensure_event_loop


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

routes = []

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
    return ensure_event_loop().run_until_complete(vellox(request))
