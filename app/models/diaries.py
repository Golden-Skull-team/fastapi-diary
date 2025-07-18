from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from enum import Enum
from app.models.base_model import BaseModel
from app.models.tags import Tags

# 모델 정의
class MoodType(str, Enum):
    glad = 'glad'
    sad = 'sad'
    angry = 'angry'
    tired = 'tired'
    annoyance = 'annoyance'
    soso = 'soso'


class Diaries(Model, BaseModel):
    user = fields.ForeignKeyField('models.users', on_delete=fields.CASCADE, null=False)
    title = fields.CharField(max_length=100, null=False)
    content = fields.TextField(null=False)
    mood = fields.CharEnumField(MoodType)
    ai_summary = fields.TextField()
    
    tags: fields.ManyToManyRelation["Tags"] = fields.ManyToManyField(
        "models.Tags",
        related_name="diaries",
        through='diary_tags'
    )

    class Meta:
        table = 'diaries'