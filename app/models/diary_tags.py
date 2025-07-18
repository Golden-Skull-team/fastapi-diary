from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from app.models.base_model import BaseModel

# 모델 정의
class DiaryTags(Model, BaseModel):
    diaries = fields.ForeignKeyField('models.diaries', on_delete=fields.CASCADE, null=False)
    tags = fields.ForeignKeyField('models.tags', on_delete=fields.CASCADE, null=False)

    class Meta:
        table = 'diary_tags'
        unique_together = (('diaries_id', 'tags_id'),)