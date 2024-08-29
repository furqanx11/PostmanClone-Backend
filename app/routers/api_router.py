from fastapi import APIRouter
from app.routers import collection, request, request_processor, response, parameter

router = APIRouter()

router.include_router(collection.router, prefix='/collection', tags=['collection'])
router.include_router(request.router, prefix='/request', tags=['request'])
router.include_router(parameter.router, prefix='/parameter', tags=['parameter'])
router.include_router(response.router, prefix='/response', tags=['response'])
router.include_router(request_processor.router, prefix='/process_request', tags=['handle_request'])