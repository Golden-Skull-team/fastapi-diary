from __future__ import annotations
from fastapi import FastAPI
from tortoise import Model, fields
from enum import Enum
from .base_model import BaseModel
from datetime import date


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

    tags = fields.ManyToManyField(
        "models.TagModel",
        related_name="diaries",
        through="diary_tag"
    )
    class Meta:
        table = 'diary'

    @classmethod
    async def create_diary(cls, url_code: str) -> DiaryModel:
        return await cls.create(url_code=url_code)
    
    @classmethod
    async def get_by_url_code(cls, url_code: str) -> DiaryModel | None:
        return await cls.filter(url_code=url_code).prefetch_related("tags").get_or_none()
    
    @classmethod
    async def get_by_user_id(cls, user_id: int):
        return await cls.filter(user_id=user_id).order_by("-created_at").all()
    
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
    
    @classmethod
    async def search_by_diary(cls, user_id: int, title: str | None, date: date | None) -> DiaryModel | None:
        qs = cls.filter(user_id=user_id)
        if title:
            qs = qs.filter(title__icontains=title)
        if date:
            qs = qs.filter(created_at__date=date)
        return await qs.order_by("created_at")
    
    @classmethod
    async def get_diary_by_tag(cls, url_code: str, tag_name: str) -> list[DiaryModel]:
        return await cls.filter(url_code=url_code, tag_name=tag_name).prefetch_related("tags")