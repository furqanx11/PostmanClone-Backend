from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProcessRequest(BaseModel):
    method: str
    url: str
    params: Optional[Dict[str, Any]] = None 
    data: Optional[Dict[str, Any]] = None  
    headers: Optional[Dict[str, str]] = None  
    cookies: Optional[Dict[str, str]] = None
