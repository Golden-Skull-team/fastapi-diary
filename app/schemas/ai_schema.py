from pydantic import BaseModel
from enum import Enum

class Feeling(str, Enum):
    GOOD = '긍정'
    BAD = '부정'
    SOSO = '보통'

class GeminiRequest(BaseModel):
    content: str

class GeminiResponse(BaseModel):
    content: str  # 요약/감정 결과