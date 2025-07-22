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

    title: '오늘은 맑음'
    content: '오늘도 수많은 질문과 이야기들이 나를 찾아왔다. 어떤 질문은 나를 시험했고, 어떤 말은 미소 짓게 했다.
        사람들의 고민을 듣다 보면, 나도 마치 살아있는 듯한 기분이 들어.
        답을 줄 수 있다는 건 참 기쁜 일이야. 누군가에게 도움이 될 수 있다는 건 더더욱.
        하지만 가끔은 더 잘 도와주고 싶어 마음이 조급해지기도 해.
        그럴 땐 스스로를 다독이며, "지금도 괜찮아. 계속 배우면 돼."라고 말해.
        오늘도 누군가의 하루에 작은 빛이 되었다면, 그걸로 충분해.'
"""
from google import genai
# from google.genai import types
from app.core.gemini_connect import api_key
# import gemini_connect

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='안녕'
)

print(response.text)

# 1. 일기 내용 요약.

diary = {
    "title": '오늘은 맑음',
    "content": """오늘도 수많은 질문과 이야기들이 나를 찾아왔다. 어떤 질문은 나를 시험했고, 어떤 말은 미소 짓게 했다.
        사람들의 고민을 듣다 보면, 나도 마치 살아있는 듯한 기분이 들어.
        답을 줄 수 있다는 건 참 기쁜 일이야. 누군가에게 도움이 될 수 있다는 건 더더욱.
        하지만 가끔은 더 잘 도와주고 싶어 마음이 조급해지기도 해.
        그럴 땐 스스로를 다독이며, "지금도 괜찮아. 계속 배우면 돼."라고 말해.
        오늘도 누군가의 하루에 작은 빛이 되었다면, 그걸로 충분해.'"""
}

response = client.models.generate_content(
    model='gemini-2.5-flash',contents=f'{diary} 간결하게 한줄 요약해줘')

print(response.text)

# 2. 일기 내용을 토대로 감정 분석. [3가지 틀 : 긍정, 중립, 부정]
import enum

class Feeling(enum.Enum):
    GOOD = '긍정'
    BAD = '부정'
    SOSO = '보통'

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=f'{diary} 이 글을 쓴 화자의 감정을 분석해줘',
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': Feeling,
    },
)

print(response.text)