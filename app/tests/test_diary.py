from datetime import date, datetime

import httpx
from httpx import AsyncClient, ASGITransport
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from tortoise.contrib.test import TestCase

from app.main import app
from app.models.diaries import Diaries


class TestDiaryRouter(TestCase):
    async def test_api_create_diary(self) -> None:
        # Given(생략)
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(url="/diarys")
        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        url_code = response.json()["url_code"]
        self.assertTrue(await Diaries.filter(url_code=url_code).exists())


class TestDiaryGet(TestCase):
    async def test_get_existing_diary(self):
        # Given
        diary = await Diaries.create(user_id=1, title="Test", content="Content", url_code="abc123")

        # When
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/diarys/{diary.url_code}")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"
        assert data["content"] == "Content"

    async def test_get_nonexistent_diary(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/diarys/not_exist")

        assert response.status_code == 404


class TestDiaryDelete(TestCase):
    async def test_delete_diary(self):
        # Given
        diary = await Diaries.create(user_id=1, title="To be deleted", url_code="delete123")

        # When
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete(f"/diarys/{diary.url_code}/delete")

        # Then
        assert response.status_code == 200
        exists = await Diaries.filter(url_code="delete123").exists()
        assert not exists


class TestDiarySearch(TestCase):
    async def test_search_by_title(self):
        await Diaries.create(user_id=1, title="My happy diary", url_code="a1")
        await Diaries.create(user_id=1, title="Sad diary", url_code="a2")

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/diarys?title=happy")

        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
        assert result[0]["title"] == "My happy diary"

    async def test_search_by_date(self):
        today = datetime.now().date()
        await Diaries.create(user_id=1, title="Today", url_code="b1", created_at=today)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/diarys?date={today}")

        assert response.status_code == 200
        result = response.json()
        assert len(result) >= 1

class TestDiaryUpdate(TestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
        self.diary = await Diaries.create(user_id=1, title="Old Title", url_code="test-title")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_update_title_success(self):
        response = await self.client.patch(
            f"/diarys/{self.diary.url_code}/title", json={"title": "Updated Title"}
        )
        assert response.status_code == 200
        await self.diary.fetch_from_db()
        assert self.diary.title == "Updated Title"
    
    async def test_update_content_success(self):
        response = await self.client.patch(
            f"/diarys/{self.diary.url_code}/content", json={"content": "New diary content"}
        )
        assert response.status_code == 200
        await self.diary.fetch_from_db()
        assert self.diary.content == "New diary content"

    async def test_update_tag_success(self):
        response = await self.client.patch(
            f"/diarys/{self.diary.url_code}/tag", json={"tags": ["travel", "fun"]}
        )
        assert response.status_code == 200

    async def test_update_mood_success(self):
        response = await self.client.patch(
            f"/diarys/{self.diary.url_code}/mood", json={"mood": "기쁨"}
        )
        assert response.status_code == 200
        await self.diary.fetch_from_db()
        assert self.diary.mood == "기쁨"