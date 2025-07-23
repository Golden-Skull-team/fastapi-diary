from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from app.schemas.ai_schema import GeminiRequest, GeminiResponse
from app.services.ai_service import service_diary_request, service_mood_analyze
import asyncio

router = APIRouter()


# 공통 텍스트 추출 유틸 함수
def extract_text(response) -> str:
    try:
        if not response.candidates:
            raise HTTPException(status_code=404, detail="Gemini가 후보 응답을 생성하지 못했습니다.")

        parts = response.candidates[0].content.parts
        if not parts:
            raise HTTPException(status_code=404, detail="Gemini 응답 내용이 비어 있습니다.")

        text = parts[0].text
        if not text.strip():
            raise HTTPException(status_code=404, detail="Gemini 요약 결과 없음.")

        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini 응답 파싱 실패: {str(e)}")


@router.post("/gemini", response_model=GeminiResponse, status_code=HTTP_201_CREATED)
async def request_gemini(gemini_data: GeminiRequest):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, service_diary_request, gemini_data.content)

    summary_text = extract_text(response)

    if not summary_text:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="요약 결과 없음")

    return GeminiResponse(content=summary_text)

@router.post("/gemini/mood", response_model=GeminiResponse, status_code=HTTP_201_CREATED)
async def request_mood(gemini_data: GeminiRequest):
    loop = asyncio.get_running_loop()
    feeling_text = await loop.run_in_executor(None, service_mood_analyze, gemini_data.content)

    if not feeling_text:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="감정 분석 결과 없음")

    return GeminiResponse(content=feeling_text)