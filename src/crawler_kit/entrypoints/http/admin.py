from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from vellox import Vellox


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
