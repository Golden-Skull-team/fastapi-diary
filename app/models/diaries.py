from __future__ import annotations
from fastapi import FastAPI
from tortoise import Model, fields
from enum import Enum
from models.base_model import BaseModel


# 모델 정의
class MoodType(Enum):
    glad = 'glad'
    sad = 'sad'
    angry = 'angry'
    tired = 'tired'
    annoyance = 'annoyance'
    soso = 'soso'


class DiaryModel(Model, BaseModel):
    url_code = fields.CharField(max_length=255, unique=True)
    user_id = fields.ForeignKeyField('models.users', on_delete=fields.CASCADE, null=False)
    title = fields.CharField(max_length=100, null=False)
    content = fields.TextField(null=False)
    mood = fields.CharEnumField(MoodType)
    ai_summary = fields.TextField()

    class Meta:
        table = 'diaries'

    @classmethod
    async def create_diary(cls, url_code: str) -> DiaryModel:
        return await cls.create(url_code=url_code)
    
    @classmethod
    async def get_by_url_code(cls, url_code: str) -> DiaryModel | None:
        return await cls.filter(url_code=url_code).get_or_none()
    
    @classmethod
    async def update_title(cls, url_code: str, title: str) -> int:
        return await cls.filter(url_code=url_code).update(title=title)

    @classmethod
    async def update_content(cls, url_code: str, content: str) -> int:
        return await cls.filter(url_code=url_code).update(content=content)

    @classmethod
    async def update_mood(cls, url_code: str, mood: str) -> int:
        return await cls.filter(url_code=url_code).update(mood=mood)
    
    @classmethod
    async def delete_diary(cls, url_code: str) -> int:
        return await cls.filter(url_code=url_code).delete()