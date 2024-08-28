from pydantic import BaseModel
from typing import Optional, List
from app.schemas.schema import BaseSchema
from app.schemas.request_schema import RequestResponse

class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CollectionResponse(BaseSchema):
    name: str
    description: Optional[str] = None
    requests: List[RequestResponse]

    class Config:
        orm_mode = True