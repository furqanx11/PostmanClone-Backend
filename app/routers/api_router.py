from fastapi import APIRouter, Depends
from app.routers import collection, request, request_processor, response, parameter, auth, protected_routes, user
from app.dependencies.auth import get_current_user

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(protected_routes.router, prefix="/protected", tags=["protected"])
router.include_router(collection.router, prefix='/collection', tags=['collection'])
router.include_router(request.router, prefix='/request', tags=['request'])
router.include_router(parameter.router, prefix='/parameter', tags=['parameter'])
router.include_router(response.router, prefix='/response', tags=['response'])
router.include_router(request_processor.router, prefix='/process_request', tags=['handle_request'])
router.include_router(user.router, prefix="/user", tags=["user"])