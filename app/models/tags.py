from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from app.models.base_model import BaseModel

# 모델 정의
class Tags(BaseModel):
    name = fields.CharField(max_length=30, null=False, unique=True)

    class Meta:
        table = 'tags'
    
    @classmethod
    async def update_tag(cls, url_code: str, tags: list[str]) -> int:
        return await cls.filter(url_code=url_code).update(tags=tags)
    
__all__ = ["Tags"]