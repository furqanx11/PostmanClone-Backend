from fastapi import APIRouter, HTTPException, Response, Cookie
import httpx
from typing import Optional
import time
from app.schemas.process_request_schema import ProcessRequest

router = APIRouter()

def set_cookie(response: Response, key: str, value: str, max_age: int = 3600):
    response.set_cookie(key=key, value=value, max_age=max_age, httponly=True)

@router.post("/")
async def send_request(
    request: ProcessRequest,
    response: Response,
    example_cookie: Optional[str] = Cookie(None)
):
    try:
        query_params = request.data.get("query_param", {})
        
        async with httpx.AsyncClient() as client:
            start_time = time.time()
            res = await client.request(
                method=request.method,
                url=request.url,
                params=query_params, 
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