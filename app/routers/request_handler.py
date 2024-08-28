from fastapi import APIRouter, HTTPException, Response, Cookie
import httpx
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time

router = APIRouter()

class RequestModel(BaseModel):
    method: str
    url: str
    params: Optional[Dict[str, Any]] = None 
    data: Optional[Dict[str, Any]] = None  
    headers: Optional[Dict[str, str]] = None  
    cookies: Optional[Dict[str, str]] = None


def set_cookie(response: Response, key: str, value: str, max_age: int = 3600):
    response.set_cookie(key=key, value=value, max_age=max_age, httponly=True)

@router.post("/send-request/")
async def send_request(
    request: RequestModel,
    response: Response,
    example_cookie: Optional[str] = Cookie(None)  
):
    try:
        async with httpx.AsyncClient() as client:
            start_time = time.time()
            res = await client.request(
                method=request.method,
                url=request.url,
                params=request.params,
                json=request.data,
                headers=request.headers,
                cookies=request.cookies
            )
            end_time = time.time()
        
        response_time = end_time - start_time
        response_size = len(res.content)
        
        set_cookie(response, "example_cookie", "abc")

        return {
            "status_code": res.status_code,
            "response_time": response_time,
            "response_size": response_size,
            "cookies": dict(res.cookies),
            "json": res.json() if res.headers.get("Content-Type") == "application/json" else res.text,
            "received_cookies": example_cookie,  
            "headers": dict(res.headers)
        }
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")
