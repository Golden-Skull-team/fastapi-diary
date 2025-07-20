from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG


class CreateDiary(BaseModel):
    model_config = FROZEN_CONFIG

    title: str
    content: str
    mood: str
    tags : list[str]