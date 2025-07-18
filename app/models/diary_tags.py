from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model

app = FastAPI()

# 모델 정의
class DiaryTags(Model):
    diaries_id = fields.ForeignKeyField('models.diaries', on_delete=fields.CASCADE, null=False)
    tags_id = fields.ForeignKeyField('models.tags', on_delete=fields.CASCADE, null=False)

    class Meta:
        table = 'diary_tags'