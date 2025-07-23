from pydantic import BaseModel
from typing import Optional
from app.schemas.frozen_config import FROZEN_CONFIG

class UserInDiary(BaseModel):
    id: int
    class Config:
        from_attributes = True

class GetDiary(BaseModel):
    model_config = {
        **FROZEN_CONFIG,
        "from_attributes": True,
    }

    url_code: str
    user: UserInDiary
    title: str
    content: str
    mood: str
    ai_summary: Optional[str]