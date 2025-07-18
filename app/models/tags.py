from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model

app = FastAPI()

# 모델 정의
class Tags(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=30, null=False, unique=True)

    class Meta:
        table = 'tags'