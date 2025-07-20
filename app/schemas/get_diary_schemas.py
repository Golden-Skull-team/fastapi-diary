from pydantic import BaseModel
from app.schemas.frozen_config import FROZEN_CONFIG

class GetDiary(BaseModel):
    model_config = FROZEN_CONFIG
    
    url_code: int
    user : int
    title : str
    content : str
    mood : str
    ai_summary : str


