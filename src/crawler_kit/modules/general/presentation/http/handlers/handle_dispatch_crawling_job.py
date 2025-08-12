from starlette.responses import JSONResponse
from starlette.requests import Request
from crawler_kit.utils.google_cloud.publish_message import publish_message
from crawler_kit.modules.general.enums.topic import Topic


async def handle_dispatch_crawling_job(request: Request):
    payload = await request.json()
    if request.path_params.get("source") == "ebay":
        if request.path_params.get("type") == "product":
            if request.path_params.get("platform") == "web":
                publish_message(Topic.Ebay, payload)
    return JSONResponse(dict(success=True, data=dict()))
