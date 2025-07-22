from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG

class Tag(BaseModel):
    model_config = FROZEN_CONFIG

    name : str