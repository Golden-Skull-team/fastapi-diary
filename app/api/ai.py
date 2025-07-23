from fastapi import APIRouter, HTTPException
from ..schemas.ai_schema import GeminiRequest
from app.models.users import Users
from app.services.ai_service import service_diary_request, service_mood_analyze
from starlette.status import HTTP_404_NOT_FOUND


router = APIRouter()

@router.post("/gemini", response_model=GeminiRequest, status_code=201)
async def request_gemini(gemini_data: GeminiRequest):
    gemini = await service_diary_request(gemini_data)
    if gemini is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'{gemini} Not Found')
    return GeminiRequest(gemini)


@router.post("/gemini/mood", response_model=GeminiRequest, status_code=201)
async def request_mood(gemini_data: GeminiRequest):
    gemini = await service_mood_analyze(gemini_data)
    if gemini is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'{gemini} Not Found')
    return GeminiRequest(gemini)