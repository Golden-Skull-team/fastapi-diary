from pydantic import BaseModel
from enum import Enum

class Feeling(Enum, BaseModel):
    GOOD: str = '긍정'
    BAD: str = '부정'
    SOSO: str = '보통'

class GeminiRequest(BaseModel):
    content: str