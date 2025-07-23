from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class TokenBlacklist(Model):
    id = fields.IntField(pk=True)
    token = fields.TextField(unique=True)
    blacklisted_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "token_blacklist"