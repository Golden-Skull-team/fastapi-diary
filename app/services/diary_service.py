from app.models.diaries import DiaryModel
from app.models.tags import TagModel
from app.utils.base62 import Base62
from app.schemas.create_diary_schemas import CreateDiary
import uuid

from typing import Optional
from datetime import date

async def service_create_diary_with_tags(create_diary: CreateDiary) -> DiaryModel:
    url_code = Base62.encode(uuid.uuid4().int)
    diary = await DiaryModel.create(
        title=create_diary.title,
        content=create_diary.content,
        mood=create_diary.mood,
        user_id=create_diary.user_id,
        url_code=url_code,
    )

    if create_diary.tags:
        tag_objs = []
        for tag_name in create_diary.tags:
            tag, _ = await TagModel.get_or_create(name=tag_name)
            tag_objs.append(tag)
        await diary.tags.add(*tag_objs)

    return diary

async def service_get_diary(url_code: str) -> DiaryModel | None:
    return await DiaryModel.get_by_url_code(url_code)

async def service_get_user_diaries(user_id: int):
    return await DiaryModel.get_by_user_id(user_id)

async def service_update_diary_title(url_code: str, title: str) -> int:
    return await DiaryModel.update_title(url_code, title)

async def service_update_diary_content(url_code: str, content: str) -> int:
    return await DiaryModel.update_content(url_code, content)

async def service_update_diary_tag(url_code: str, tags: list[str]) -> int:
    return await TagModel.update_tag(url_code, tags)

async def service_update_diary_mood(url_code: str, mood: str) -> int:
    return await DiaryModel.update_mood(url_code, mood)

async def service_delete_diary(url_code: str):
    return await DiaryModel.delete_diary(url_code)

async def service_search_diaries(user_id: int, title: Optional[str] | None, date:Optional[date] | None):
    return await DiaryModel.search_by_diary(user_id, title, date)

async def service_get_diary_by_tag(url_code: str, tag_name: str) -> list[DiaryModel]:
    return await DiaryModel.get_diary_by_tag(url_code, tag_name)