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

class User(BaseModel):
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ["hashed_password"]

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
Collection_Pydantic = pydantic_model_creator(Collection, name="Collection")
Request_Pydantic = pydantic_model_creator(Request, name="Request")
Parameter_Pydantic = pydantic_model_creator(Parameter, name="Parameter")
Response_Pydantic = pydantic_model_creator(Response, name="Response")
