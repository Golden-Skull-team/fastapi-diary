from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from app.models.base_model import BaseModel

# 모델 정의
class Tags(BaseModel):
    name = fields.CharField(max_length=30, null=False, unique=True)
    url_code = fields.CharField(
    max_length=255, null=False, unique=True, default=True
)
    class Meta:
        table = 'tags'
        
__all__ = ["Tags"]
