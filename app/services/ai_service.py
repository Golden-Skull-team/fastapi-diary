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
# from app.core.gemini_connect import api_key
# from gemini_connect import api_key
from app.core.config import Settings
from app.schemas import ai_schema
# import promp
from app.services.prompt import request_prompt, mood_analyze_prompt

client = genai.Client(api_key=Settings.GEMINI_API_KEY)
# client = genai.Client(api_key='')



# 요약
def service_diary_request():
    question = request_prompt()
    # question = prompt.req_t()
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents=question
    )
    # print(response)
    return response

# 감정분석
feelings = [e.value for e in ai_schema.Feeling]

def service_mood_analyze(feelings):
    question = mood_analyze_prompt()
    # question = prompt.ana_t()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question,
        config={
            'response_mime_type': 'text/x.enum',
            'response_schema': feelings,
        },
    )
    # print(response)
    return response