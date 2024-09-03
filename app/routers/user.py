from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.schemas.user_schema import UserOut
from app.models import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user