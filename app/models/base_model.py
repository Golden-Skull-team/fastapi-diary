from tortoise import fields
from tortoise.models import Model

class BaseModel(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    
    class Meta:
        abstract = True