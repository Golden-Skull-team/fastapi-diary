from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# 회원가입 요청
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nickname: str = Field(..., min_length=2, max_length=30)
    username: str = Field(..., min_length=2, max_length=30)
    phone_number: Optional[str] = Field(None, max_length=15)


# 로그인 요청
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


# 로그인 성공 시 토큰 응답
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 회원가입/내 정보 응답
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    username: str


class UserDetailSchema(UserResponseSchema):
    phone_number: Optional[str]
    is_active: bool
    is_staff: bool
    is_admin: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]