import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # FastAPI 인스턴스 import
from app.schemas.user import UserCreateSchema

@pytest.mark.anyio
async def test_register_user_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/users", json={
            "username": "diary",
            "nickname": "다이어리유저",
            "email": "testuser@example.com",
            "password": "securepassword",
            "phone_number": "01012345678"
        })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["username"] == "diary"
    assert data["nickname"] == "다이어리유저"
    assert "id" in data


@pytest.mark.anyio
async def test_register_user_duplicate_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 먼저 회원가입 진행
        await client.post("/users", json={
            "username": "user1",
            "nickname": "닉네임1",
            "email": "dup@example.com",
            "password": "password123",
            "phone_number": "01011112222"
        })

        # 같은 이메일로 다시 회원가입 시도
        response = await client.post("/users", json={
            "username": "user2",
            "nickname": "닉네임2",
            "email": "dup@example.com",
            "password": "password456",
            "phone_number": "01033334444"
        })

    assert response.status_code == 400
    assert response.json() == {"detail": "이미 존재하는 이메일입니다."}
