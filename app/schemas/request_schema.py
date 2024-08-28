from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.schemas.schema import BaseSchema
from app.schemas.parameter_schema import ParameterResponse
from app.schemas.response_schema import ResponseResponse

class RequestCreate(BaseModel):
    collection_id: int
    name: str
    method: str
    url: str
    saved_at: Optional[datetime] = None

    @validator('collection_id')
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise ValueError('collection_id must be an integer')
        return v

class RequestUpdate(BaseModel):
    collection_id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    method: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    saved_at: Optional[str] = Field(None)

    @validator('collection_id')
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise ValueError('collection_id must be an integer')
        return v

    class Config:
        orm_mode = True

class RequestResponse(BaseSchema):
    collection_id: int
    name: str
    method: str
    url: str
    saved_at: Optional[datetime] = None
    parameters: List[ParameterResponse]
    responses: List[ResponseResponse]

    @validator('collection_id')
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise ValueError('collection_id must be an integer')
        return v

    class Config:
        orm_mode = True