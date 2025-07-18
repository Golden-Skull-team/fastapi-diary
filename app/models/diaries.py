from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from enum import Enum

app = FastAPI()

# 모델 정의
class MoodType(Enum):
    glad = 'glad'
    sad = 'sad'
    angry = 'angry'
    tired = 'tired'
    annoyance = 'annoyance'
    soso = 'soso'


class Diaries(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.ForeignKeyField('models.users', on_delete=fields.CASCADE, null=False)
    title = fields.CharField(max_length=100, null=False)
    content = fields.TextField(null=False)
    mood = fields.CharEnumField(MoodType)
    ai_summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True, null=True)

    class Meta:
        table = 'diaries'