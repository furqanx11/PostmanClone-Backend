from pydantic import BaseModel, validator
from typing import Optional
from app.schemas.schema import BaseSchema
from app.exceptions.custom_exceptions import CustomValidationException

class ResponseCreate(BaseModel):
    request_id: int
    status_code: int
    body: str
    response_time: float
    response_size: int

    @validator('request_id', pre = True)
    def validate_request_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v

class ResponseUpdate(BaseModel):
    request_id: Optional[int] = None
    status_code: Optional[int] = None
    body: Optional[str] = None
    response_time: Optional[float] = None
    response_size: Optional[int] = None

    @validator('request_id')
    def validate_request_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v

class ResponseResponse(BaseSchema):
    request_id: int
    status_code: int
    body: str
    response_time: float
    response_size: int

    @validator('request_id')
    def validate_request_id(cls, v):
        if not isinstance(v, int):
            raise CustomValidationException(status_code=422, detail='request_id must be an integer')
        return v