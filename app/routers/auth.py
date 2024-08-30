from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User, User_Pydantic
from app.schemas.user_schema import UserCreate, UserOut
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    user_obj = await User.create(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}