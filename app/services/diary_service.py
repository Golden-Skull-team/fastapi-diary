from app.models.diaries import DiaryModel
from app.models.tags import TagsModel
from app.utils.base62 import Base62
import uuid


async def service_create_diary() -> DiaryModel:
    return await DiaryModel.create_diary(Base62.encode(uuid.uuid4().int))

async def service_get_diary(url_code: str) -> DiaryModel | None:
    return await DiaryModel.get_by_url_code(url_code)

async def service_update_diary_title(url_code: str, title: str) -> int:
    return await DiaryModel.update_title(url_code, title)

async def service_update_diary_content(url_code: str, content: str) -> int:
    return await DiaryModel.update_content(url_code, content)

async def service_update_diary_tag(url_code: str, tags: list[str]) -> int:
    return await TagsModel.update_tag(url_code, tags)

async def service_update_diary_mood(url_code: str, mood: str) -> int:
    return await DiaryModel.update_mood(url_code, mood)

async def service_delete_diary(url_code: str):
    return await DiaryModel.delete_diary(url_code)