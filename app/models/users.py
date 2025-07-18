from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model

app = FastAPI()

# 모델 정의
class Users(Model):
    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255, null=False)
    nickname = fields.CharField(max_length=30, null=False)
    username = fields.CharField(max_length=30)
    phone_number = fields.CharField(max_length=15)
    last_login = fields.DatetimeField(null=True, ) # ???????
    is_staff = fields.BooleanField(defalut=False)
    is_admin = fields.BooleanField(defalut=False)
    is_active = fields.BooleanField(defalut=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True, null=True)

    class Meta:
        table = 'users'