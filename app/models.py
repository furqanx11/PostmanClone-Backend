from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class Collection(BaseModel):
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    requests = fields.ReverseRelation["Request"]

class Request(BaseModel):
    collection = fields.ForeignKeyField("models.Collection", related_name="requests", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=50)
    method = fields.CharField(max_length=10)
    url = fields.CharField(max_length=255)
    saved_at = fields.DatetimeField(null=True)
    parameters = fields.ReverseRelation["Parameter"]
    responses = fields.ReverseRelation["Response"]

class Parameter(BaseModel):
    request = fields.ForeignKeyField("models.Request", related_name="parameters", on_delete=fields.CASCADE)
    query_param = fields.CharField(max_length=50, null = True)
    body = fields.TextField(null=True)

class Response(BaseModel):
    request = fields.ForeignKeyField("models.Request", related_name="responses", on_delete=fields.CASCADE)
    status_code = fields.IntField()
    body = fields.TextField()
    response_time = fields.FloatField()
    response_size = fields.IntField()

