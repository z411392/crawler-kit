from starlette.responses import JSONResponse
from starlette.requests import Request
from crawler_kit.utils.google_cloud.publish_message import publish_message
from crawler_kit.modules.general.enums.topic import Topic
from logging import getLogger

logger = getLogger(__name__)


async def handle_dispatch_crawling_job(request: Request):
    payload = await request.json()
    logger.info(f"dispatching crawling job: {payload}")
    print(f"dispatching crawling job: {payload}")
    if request.path_params.get("source") == "ebay":
        if request.path_params.get("type") == "product":
            if request.path_params.get("platform") == "web":
                publish_message(Topic.Ebay, payload)
    # if request.path_params.get("source") == "amazon":
    #     if request.path_params.get("type") == "product":
    #         if request.path_params.get("platform") == "web":
    #             publish_message(Topic.Amazon, payload)
    if request.path_params.get("source") == "lazada":
        if request.path_params.get("type") == "product":
            if request.path_params.get("platform") == "web":
                publish_message(Topic.Lazada, payload)
    return JSONResponse(dict(success=True, data=dict()))
