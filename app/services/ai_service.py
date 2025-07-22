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
from gemini_connect import api_key
import prompt

client = genai.Client(api_key=api_key)


# 요약
def diary_request():
    # request = prompt.request_prompt()
    question = prompt.req_t()    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question
    )
    print(response)

diary_request()
