from fastapi import APIRouter, HTTPException, Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)
from app.schemas.create_diary_schemas import CreateDiary, DiaryResponse
from app.schemas.get_diary_schemas import GetDiary
from app.schemas.update_diary_schemas import (
    UpdateDiaryTitle,
    UpdateDiaryContent,
    UpdateDiaryTag,
    UpdateDiaryMood
)
from app.services.diary_service import (
    service_create_diary_with_tags,
    service_get_diary,
    service_update_diary_title,
    service_update_diary_content,
    service_update_diary_tag,
    service_update_diary_mood,
    service_delete_diary,
    service_get_user_diaries,
    service_search_diaries,
    service_get_diary_by_tag
)

from typing import Optional
from datetime import date
from app.models.users import Users
from app.models.diaries import Diaries
from app.core.dependencies.auth import get_current_user

diary_router = APIRouter(prefix="/diaries", tags=["Diary"])


@diary_router.post("/", response_model=DiaryResponse, description="Diary 생성")
async def api_create_diary(
    create_diary: CreateDiary,
    current_user: Users = Depends(get_current_user),
):
    diary = await service_create_diary_with_tags(create_diary, current_user.id)
    return diary 


@diary_router.get("/latest", description="내가 쓴 일기 전체 조회 (최신순)")
async def api_get_my_diaries(current_user: Users = Depends(get_current_user)) -> list[GetDiary]:
    diaries = await service_get_user_diaries(current_user.id)
    return [GetDiary.model_validate(d) for d in diaries]


@diary_router.get("/{diary_url_code}", description="Diary 조회")
async def api_get_diary(diary_url_code: str) -> GetDiary:
    diary = await service_get_diary(diary_url_code)
    if diary is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return GetDiary.model_validate(diary)


@diary_router.patch("/{diary_url_code}/title", description="Diary 제목 수정")
async def api_update_diary_title(
    diary_url_code: str,
    update_data: UpdateDiaryTitle
) -> GetDiary:
    await service_update_diary_title(diary_url_code, update_data.title)
    updated = await service_get_diary(diary_url_code)
    if updated is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return GetDiary.model_validate(updated)


@diary_router.patch("/{diary_url_code}/content", description="Diary 내용 수정")
async def api_update_diary_content(
    diary_url_code: str,
    update_data: UpdateDiaryContent
) -> GetDiary:
    await service_update_diary_content(diary_url_code, update_data.content)
    updated = await service_get_diary(diary_url_code)
    if updated is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return GetDiary.model_validate(updated)


@diary_router.patch("/{diary_url_code}/tag", description="Diary 태그 수정")
async def api_update_diary_tag(
    diary_url_code: str,
    update_data: UpdateDiaryTag
) -> GetDiary:
    await service_update_diary_tag(diary_url_code, update_data.tags)
    updated = await service_get_diary(diary_url_code)
    if updated is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return GetDiary.model_validate(updated)


@diary_router.patch("/{diary_url_code}/mood", description="Diary 감정 수정")
async def api_update_diary_mood(
    diary_url_code: str,
    update_data: UpdateDiaryMood
) -> GetDiary:
    await service_update_diary_mood(diary_url_code, update_data.mood)
    updated = await service_get_diary(diary_url_code)
    if updated is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return GetDiary.model_validate(updated)


@diary_router.delete("/{diary_url_code}/delete", description="Diary 삭제")
async def api_delete_diary(diary_url_code: str):
    deleted = await service_delete_diary(diary_url_code)
    if deleted is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Diary not found")
    return {"message": "Diary deleted successfully"}


@diary_router.get("/search", description="제목 또는 날짜로 일기 검색")
async def api_search_diaries(
    title: Optional[str] = None,
    date: Optional[date] = Depends(),
    current_user: Users = Depends(get_current_user)
) -> list[GetDiary]:
    diaries = await service_search_diaries(current_user.id, title, date)
    return [GetDiary.model_validate(d) for d in diaries]


@diary_router.get("/{tag_name}/diaries", description="태그로 일기 검색")
async def api_search_diaries_tag(
    tag_name: str,
    current_user: Users = Depends(get_current_user)
) -> list[GetDiary]:
    diaries = await service_get_diary_by_tag(current_user.id, tag_name)
    return [GetDiary.model_validate(d) for d in diaries]
