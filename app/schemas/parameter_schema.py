from pydantic import BaseModel, validator
from typing import Optional
from app.schemas.schema import BaseSchema
from app.exceptions.custom_exceptions import CustomValidationException, custom_validation_exception_handler

class ParameterCreate(BaseModel):
    request_id: int
    query_param: Optional[str] = None
    body: Optional[str] = None

    @validator('request_id', pre=True)
    def validate_request_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v


class ParameterUpdate(BaseModel):
    request_id: Optional[int] = None
    query_param: Optional[str] = None
    body: Optional[str] = None

    @validator('request_id')
    def validate_request_id(cls, v):
        if v is not None and not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v


class ParameterResponse(BaseSchema):
    request_id: int
    query_param: Optional[str] = None
    body: Optional[str] = None

    @validator('request_id')
    def validate_request_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v