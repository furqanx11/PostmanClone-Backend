from fastapi import FastAPI
from app.routers import collection
from app.routers.api_router import router
from app.middleware.cors import cors_middleware
from app.exceptions import CustomValidationException
from app.db import init, close
#from app.exceptions.custom_exceptions import custom_validation_exception_handler
from app.exceptions.custom_exceptions import custom_validation_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError


app = FastAPI()

cors_middleware(app)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomValidationException, custom_validation_exception_handler)
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init()
    await collection.get_all_collections()

@app.on_event("shutdown")
async def shutdown_event():
    await close()

@app.get("/")
async def read_root():
    collections = await collection.get_all_collections()
    return collections