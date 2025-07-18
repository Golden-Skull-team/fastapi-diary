from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from app.models.base_model import BaseModel

# 모델 정의
class Users(Model, BaseModel):
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255, null=False)
    nickname = fields.CharField(max_length=30, null=False)
    username = fields.CharField(max_length=30, null=False)
    phone_number = fields.CharField(max_length=15, null=False)
    last_login = fields.DatetimeField(null=True) # ???????
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = 'users'