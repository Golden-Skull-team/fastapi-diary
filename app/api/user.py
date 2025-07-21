import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
from ..schemas.user import UserCreateSchema, UserResponseSchema
from app.models.users import User
from utils.security import hash_password

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5)

@router.post("/users", response_model=UserResponseSchema, status_code=201)
async def register_user(user_data: UserCreateSchema):
    existing_user = await User.get_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    loop = asyncio.get_running_loop()
    hashed_pw = await loop.run_in_executor(executor, hash_password, user_data.password)

    user = await User.create(
        email=user_data.email,
        password=hashed_pw,
        nickname=user_data.nickname,
        username=user_data.username,
        phone_number=user_data.phone_number,
    )

    user_schema = UserResponseSchema.model_validate(user)
    return user_schema