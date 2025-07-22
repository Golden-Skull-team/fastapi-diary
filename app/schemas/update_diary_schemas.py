from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG

class UpdateDiaryTitle(BaseModel):
    model_config = FROZEN_CONFIG

    title : str


class UpdateDiaryContent(BaseModel):
    model_config = FROZEN_CONFIG

    content : str


class UpdateDiaryTag(BaseModel):
    model_config = FROZEN_CONFIG

    tags : list[str]


class UpdateDiaryMood(BaseModel):
    model_config = FROZEN_CONFIG

    mood : str
