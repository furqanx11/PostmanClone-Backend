from pydantic import BaseModel, Field, validator, StrictInt
from typing import Optional, List
from datetime import datetime
from app.schemas.schema import BaseSchema
from app.schemas.parameter_schema import ParameterResponse
from app.schemas.response_schema import ResponseResponse
from app.exceptions.custom_exceptions import custom_validation_exception_handler, CustomValidationException

class RequestCreate(BaseModel):
    collection_id: StrictInt
    name: str
    method: str
    url: str
    saved_at: Optional[datetime] = None

    @validator('collection_id', pre = True)
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='collection_id must be an integer')
        return v

class RequestUpdate(BaseModel):
    collection_id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    method: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    saved_at: Optional[str] = Field(None)

    @validator('collection_id', pre = True)
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
           raise CustomValidationException(status_code=422, detail='collection_id must be an integer')
        return v

    class Config:
        orm_mode = True

class RequestResponse(BaseSchema):
    collection_id: int
    name: str
    method: str
    url: str
    saved_at: Optional[datetime] = None
    parameters: Optional[List[ParameterResponse]] = None
    responses: Optional[List[ResponseResponse]] = None

    @validator('collection_id', pre = True)
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='collection_id must be an integer')
        return v

    class Config:
        orm_mode = True

class Request_Response(BaseSchema):
    collection_id: int
    name: str
    method: str
    url: str
    saved_at: Optional[datetime] = None

    @validator('collection_id', pre = True)
    def validate_collection_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='collection_id must be an integer')
        return v

    class Config:
        orm_mode = True