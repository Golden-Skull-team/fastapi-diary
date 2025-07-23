import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from app.models.users import Users
from ..utils.security import hash_password
from app.core.dependencies.auth import get_current_user

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5)

@router.post("/users", response_model=UserResponseSchema, status_code=201)
async def register_user(user_data: UserCreateSchema):
    existing_user = await Users.get_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    loop = asyncio.get_running_loop()
    hashed_pw = await loop.run_in_executor(executor, hash_password, user_data.password)

    user = await Users.create(
        email=user_data.email,
        password=hashed_pw,
        nickname=user_data.nickname,
        username=user_data.username,
        phone_number=user_data.phone_number,
    )

    user_schema = UserResponseSchema.model_validate(user)
    return user_schema

# 내 정보 조회
@router.get("/me", response_model=UserResponseSchema)
async def get_me(current_user: Users = Depends(get_current_user)):
    return current_user

# 회원정보 수정
@router.patch("/me", response_model=UserResponseSchema)
async def update_me(update_data: UserUpdateSchema, current_user: Users = Depends(get_current_user)):
    update_dict = update_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="수정할 항목이 없습니다.")

    for field, value in update_dict.items():
        setattr(current_user, field, value)

    await current_user.save()
    return current_user

# 회원 탈퇴
@router.delete("/me", status_code=200)
async def delete_me(current_user: Users = Depends(get_current_user)):
    await current_user.delete()
    return {"detail": "Deleted successfully"}