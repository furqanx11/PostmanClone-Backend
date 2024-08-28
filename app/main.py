from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise
from app.config import settings
from app.routers import collection, request, request_handler, response, parameter
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import CustomValidationException
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


register_tortoise(
    app,
    db_url= "postgres://username:password@localhost:5432/dbname",
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.exception_handler(CustomValidationException)
async def custom_validation_exception_handler(request: Request, exc: CustomValidationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(collection.router, prefix = '/collection', tags = ['collection'])
app.include_router(request.router, prefix = '/request', tags = ['request'])
app.include_router(parameter.router, prefix = '/parameter', tags = ['parameter'])
app.include_router(response.router, prefix = '/response', tags = ['response'])
app.include_router(request_handler.router, prefix = '/handle_request', tags = ['handle_request'])
@app.on_event("startup")
async def startup_event():
    await collection.get_all_collections()

@app.get("/")
async def read_root():
    collections = await collection.get_all_collections()
    return collections
