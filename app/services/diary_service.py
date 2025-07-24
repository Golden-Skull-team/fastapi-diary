from app.models.diaries import Diaries
from app.models.tags import Tags
from app.utils.base62 import Base62
from app.schemas.create_diary_schemas import CreateDiary
import uuid
from typing import Optional
from datetime import date


# ✅ 일기 생성
async def service_create_diary_with_tags(create_diary: CreateDiary, user_id: int) -> Diaries:
    url_code = Base62.encode(uuid.uuid4().int)
    diary = await Diaries.create(
        title=create_diary.title,
        content=create_diary.content,
        mood=create_diary.mood,
        user_id=user_id,
        url_code=url_code,
    )

    if create_diary.tags:
        tag_objs = []
        for tag_name in create_diary.tags:
            tag, _ = await Tags.get_or_create(name=tag_name)
            tag_objs.append(tag)
        await diary.tags.add(*tag_objs)

    return diary


# ✅ 단일 조회 (user dict, mood string 변환)
async def service_get_diary(url_code: str) -> dict | None:
    results = await Diaries.filter(url_code=url_code).values(
        "url_code", "user_id", "title", "content", "mood", "ai_summary"
    )
    if results:
        diary = results[0]

        user_id_value = diary.get("user_id")
        diary["user"] = {"id": int(user_id_value)} if user_id_value is not None else {"id": 0}

        mood_value = diary.get("mood")
        if hasattr(mood_value, "value"):
            diary["mood"] = mood_value.value

        return diary

    return None


# ✅ 전체 조회 (user dict, mood string 변환)
async def service_get_user_diaries(user_id: int) -> list[dict]:
    diaries = await Diaries.filter(user_id=user_id).order_by("-id").values(
        "url_code", "user_id", "title", "content", "mood", "ai_summary"
    )

    for diary in diaries:
        user_id_value = diary.get("user_id")
        diary["user"] = {"id": int(user_id_value)} if user_id_value is not None else {"id": 0}

        mood_value = diary.get("mood")
        if hasattr(mood_value, "value"):
            diary["mood"] = mood_value.value

    return diaries


# ✅ 제목 수정
async def service_update_diary_title(url_code: str, title: str) -> int:
    return await Diaries.update_title(url_code, title)


# ✅ 본문 수정
async def service_update_diary_content(url_code: str, content: str) -> int:
    return await Diaries.update_content(url_code, content)


# ✅ 태그 수정
async def service_update_diary_tag(url_code: str, tags: list[str]) -> int:
    return await Tags.update_tag(url_code, tags)


# ✅ 기분 수정
async def service_update_diary_mood(url_code: str, mood: str) -> int:
    return await Diaries.update_mood(url_code, mood)


# ✅ 일기 삭제
async def service_delete_diary(url_code: str):
    return await Diaries.delete_diary(url_code)


# ✅ 검색 (user dict, mood string 변환)
async def service_search_diaries(user_id: int, title: Optional[str], date: Optional[date]) -> list[dict]:
    diaries = await Diaries.search_by_diary(user_id, title, date).values(
        "url_code", "user_id", "title", "content", "mood", "ai_summary"
    )

    for diary in diaries:
        user_id_value = diary.get("user_id")
        diary["user"] = {"id": int(user_id_value)} if user_id_value is not None else {"id": 0}

        mood_value = diary.get("mood")
        if hasattr(mood_value, "value"):
            diary["mood"] = mood_value.value

    return diaries


# ✅ 태그 기반 조회 (user dict, mood string 변환)
async def service_get_diary_by_tag(user_id: int, tag_name: str) -> list[dict]:
    diaries = await Diaries.get_diary_by_tag(user_id, tag_name).values(
        "url_code", "user_id", "title", "content", "mood", "ai_summary"
    )

    for diary in diaries:
        user_id_value = diary.get("user_id")
        diary["user"] = {"id": int(user_id_value)} if user_id_value is not None else {"id": 0}

        mood_value = diary.get("mood")
        if hasattr(mood_value, "value"):
            diary["mood"] = mood_value.value

    return diaries
