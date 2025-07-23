"""
schemas/create_diary_schema.py
from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG


class CreateDiary(BaseModel):
    model_config = FROZEN_CONFIG

    title: str
    content: str
    mood: str
    tags : list[str]
"""

from google import genai
from app.core.config import Settings
from app.schemas import ai_schema
from app.services.prompt import request_prompt, mood_analyze_prompt

client = genai.Client(api_key=Settings.GEMINI_API_KEY)

# 요약
def service_diary_request(diary_content: str):
    question = request_prompt(diary_content)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question
    )
    return response

# 감정분석
feelings = [e.value for e in ai_schema.Feeling]

def service_mood_analyze(diary_content: str) -> str:
    question = mood_analyze_prompt(diary_content)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question,
        config={
            'response_mime_type': 'text/x.enum',
            'response_schema': ai_schema.Feeling,
        },
    )

    try:
        return response.candidates[0].content.parts[0].text
    except (AttributeError, IndexError):
        raise ValueError("감정 분석 결과를 추출할 수 없습니다.")