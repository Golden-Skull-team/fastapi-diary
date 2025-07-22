from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from app.models.base_model import BaseModel

# 모델 정의
class DiaryTags(BaseModel):
    diary = fields.ForeignKeyField('models.Diaries', on_delete=fields.CASCADE, null=False)
    tag = fields.ForeignKeyField('models.Tags', on_delete=fields.CASCADE, null=False)

    class Meta:
        table = 'diary_tags'
        unique_together = (('diary_id', 'tag_id'),)

__all__ = ["DiaryTags"]