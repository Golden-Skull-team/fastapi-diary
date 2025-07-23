import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from tortoise import Tortoise
from app.api.user import router as user_router

# 테스트용 FastAPI 앱
app_for_testing = FastAPI()
app_for_testing.include_router(user_router)

# 테스트용 Tortoise ORM 설정
TORTOISE_ORM_TEST = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init_test_db():
    """테스트 DB 초기화"""
    await Tortoise.init(config=TORTOISE_ORM_TEST)
    await Tortoise.generate_schemas()

async def cleanup_test_db():
    """테스트 DB 정리"""
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_register_user_success():
    # 테스트 시작 전 DB 초기화
    await init_test_db()
    
    try:
        async with AsyncClient(transport=ASGITransport(app=app_for_testing), base_url="http://test") as client:
            # 모든 필수 필드 포함
            response = await client.post("/users", json={
                "email": "test@example.com",
                "password": "password123",  # 8자 이상
                "nickname": "testnick",     # 2-30자
                "username": "testuser",     # 2-30자
                "phone_number": "01012345678"  # 최대 15자
            })
            
            print(f"\n=== 🔍 응답 디버깅 ===")
            print(f"상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
            
            if response.status_code == 422:
                print(f"유효성 검사 오류 세부사항: {response.json()}")
            
            assert response.status_code == 201
    finally:
        # 테스트 완료 후 DB 정리
        await cleanup_test_db()

@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    # 테스트 시작 전 DB 초기화
    await init_test_db()
    
    try:
        async with AsyncClient(transport=ASGITransport(app=app_for_testing), base_url="http://test") as client:
            # 첫 번째 사용자 생성
            user_data = {
                "email": "duplicate@example.com",
                "password": "password123",
                "nickname": "duplicate1",
                "username": "dupuser1", 
                "phone_number": "01011111111"
            }
            
            first_response = await client.post("/users", json=user_data)
            print(f"첫 번째 등록 응답: {first_response.status_code}")
            
            # 중복 이메일로 두 번째 사용자 생성 시도 (다른 필드는 변경)
            duplicate_data = {
                "email": "duplicate@example.com",  # 같은 이메일
                "password": "password456", 
                "nickname": "duplicate2",
                "username": "dupuser2",
                "phone_number": "01022222222"
            }
            
            second_response = await client.post("/users", json=duplicate_data)
            print(f"중복 등록 응답: {second_response.status_code}")
            print(f"중복 등록 응답 내용: {second_response.text}")
            
            assert second_response.status_code == 400
    finally:
        # 테스트 완료 후 DB 정리
        await cleanup_test_db()

@pytest.mark.asyncio 
async def test_register_user_validation_errors():
    """유효성 검사 오류 테스트"""
    # 테스트 시작 전 DB 초기화
    await init_test_db()
    
    try:
        async with AsyncClient(transport=ASGITransport(app=app_for_testing), base_url="http://test") as client:
            # 비밀번호 너무 짧음
            response = await client.post("/users", json={
                "email": "test@example.com",
                "password": "short",  # 8자 미만
                "nickname": "nick",
                "username": "user",
                "phone_number": "01012345678"
            })
            assert response.status_code == 422
            
            # 잘못된 이메일 형식
            response = await client.post("/users", json={
                "email": "invalid-email",  # 잘못된 형식
                "password": "password123",
                "nickname": "nick",
                "username": "user", 
                "phone_number": "01012345678"
            })
            assert response.status_code == 422
            
            # 닉네임 너무 짧음
            response = await client.post("/users", json={
                "email": "test@example.com",
                "password": "password123",
                "nickname": "a",  # 2자 미만
                "username": "user",
                "phone_number": "01012345678"
            })
            assert response.status_code == 422
    finally:
        # 테스트 완료 후 DB 정리
        await cleanup_test_db()