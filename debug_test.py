import asyncio
import pytest
from tortoise import Tortoise

TORTOISE_ORM_TEST = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

@pytest.mark.asyncio
async def test_tortoise_connection():
    try:
        print("🔄 Tortoise ORM 초기화 시도...")
        await Tortoise.init(config=TORTOISE_ORM_TEST)
        print("✅ Tortoise ORM 초기화 성공!")
        
        print("🔄 스키마 생성 시도...")
        await Tortoise.generate_schemas()
        print("✅ 스키마 생성 성공!")
        
        print("🔄 Users 모델 테스트...")
        from app.models.users import Users
        
        # 테스트 사용자 생성
        user = await Users.create(
            email="test@example.com",
            password="hashedpassword",
            nickname="testuser",
            username="testuser",
            phone_number="01012345678"
        )
        print(f"✅ 사용자 생성 성공! ID: {user.id}")
        
        # 사용자 조회
        found_user = await Users.get_or_none(email="test@example.com")
        print(f"✅ 사용자 조회 성공! 닉네임: {found_user.nickname}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()
        print("🔚 연결 종료")

if __name__ == "__main__":
    asyncio.run(test_tortoise_connection())