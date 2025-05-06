from fastapi import APIRouter
from helper.baseResponse import BaseResponse
from controller.data_controller import router as data_router
from controller.ai_controller import router as ai_router

router = APIRouter()

base_urls = "/api"

router.include_router(data_router, prefix=base_urls)
router.include_router(ai_router, prefix=base_urls)

@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["data"])
async def not_route_found(full_path: str):
    return BaseResponse('notfound', 'No Route Found')
