from fastapi.responses import JSONResponse
from fastapi import Request, Response
#from app.exceptions import CustomValidationException


class CustomValidationException(Exception):
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail

async def custom_validation_exception_handler(request: Request, exc: CustomValidationException):
        if exc.status_code == 204:
             return Response(
                  status_code=exc.status_code
             )
        else:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
