from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


