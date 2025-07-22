from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG


class DiaryTag(BaseModel):
    model_config = FROZEN_CONFIG

    diaries : int
    tags : list[str]