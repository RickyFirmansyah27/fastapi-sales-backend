import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from config.ai_config import call_ai
from helper.baseResponse import BaseResponse

router = APIRouter()
logger = logging.getLogger("response")

class RequestBody(BaseModel):
    prompt: str  # pastikan prompt adalah string


@router.post("/ai", tags=["data"])
async def post_ai_conservation(request_body: RequestBody):
    try:
        prompt = request_body.prompt
        result = call_ai(prompt)

        logger.info(f'[AiController] - Successfully fetched ai content.')
        return BaseResponse('success', 'Successfully fetched ai content', {"chatAi": result})

    except Exception as e:
        logger.error('[AiController] - Failed to fetch ai content.', exc_info=True)
        return BaseResponse('error', 'Failed to fetch ai content', str(e))
