from fastapi import APIRouter, Request, Response, HTTPException, status
from app.schemas.user import UserLoginSchema, TokenResponseSchema
from app.models.users import Users
from app.utils.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.models.token_blacklist import TokenBlacklist
from jose import JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=TokenResponseSchema)
async def login_user(user_data: UserLoginSchema, response: Response):
    user = await Users.get_or_none(email=user_data.email)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # access, refresh 토큰 생성
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Refresh Token을 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7일
    )

    return TokenResponseSchema(access_token=access_token)

@router.post("/logout", status_code=204)
async def logout_user(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token not found in cookie")

    # 유효한 JWT인지 확인
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 이미 블랙리스트에 있는지 확인
    if await TokenBlacklist.get_or_none(token=refresh_token):
        raise HTTPException(status_code=400, detail="Token already blacklisted")

    # DB에 저장 (블랙리스트 등록)
    await TokenBlacklist.create(token=refresh_token)

    # 쿠키 삭제
    response.delete_cookie(key="refresh_token")

    return