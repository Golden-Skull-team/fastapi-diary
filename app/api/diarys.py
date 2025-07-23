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
from app.core.dependencies.auth import get_current_user

diary_router = APIRouter(prefix="/diaries", tags=["Diary"])


@diary_router.post("/", response_model=DiaryResponse, description="Diary 생성")
async def api_create_diary(
    create_diary: CreateDiary,
    current_user: Users = Depends(get_current_user),
):
    diary = await service_create_diary_with_tags(create_diary, current_user.id)
    return diary 


@diary_router.get("/{diary_url_code}", description="Diary 조회")
async def api_get_diary(diary_url_code: str) -> GetDiary:
    diary = await service_get_diary(diary_url_code)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)


@diary_router.get("/", description="내가 쓴 일기 전체 조회 (최신순)") # get_current_user
async def api_get_my_diaries(current_user: Users = Depends()) -> list[GetDiary]: # 대상우 도와줘
    diaries = await service_get_user_diaries(current_user.id)
    return [GetDiary(diary) for diary in diaries]


@diary_router.patch("/{diary_url_code}/title", description="diary title를 수정합니다.")
async def api_update_diary_title(
    diary_url_code: str, update_diary_title: UpdateDiaryTitle
) -> GetDiary:
    diary = await service_update_diary_title(diary_url_code, update_diary_title)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)


@diary_router.patch("/{diary_url_code}/content", description="diary content를 수정합니다.")
async def api_update_diary_content(
    diary_url_code: str, update_diary_Conent: UpdateDiaryContent
) -> GetDiary:
    diary = await service_update_diary_content(diary_url_code, update_diary_Conent)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)

@diary_router.patch("/{diary_url_code}/tag", description="diary tag를 수정합니다.")
async def api_update_diary_tag(
    diary_url_code: str, update_diary_Tag: UpdateDiaryTag
) -> GetDiary:
    diary = await service_update_diary_tag(diary_url_code, update_diary_Tag)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)

@diary_router.patch("/{diary_url_code}/mood", description="diary mood를 수정합니다.")
async def api_update_diary_mood(
    diary_url_code: str, update_diary_Mood: UpdateDiaryMood
) -> GetDiary:
    diary = await service_update_diary_mood(diary_url_code, update_diary_Mood)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)


@diary_router.delete("/{diary_url_code}/delete", description="diary를 삭제합니다.")
async def api_delete_diary(diary_url_code: str):
    diary = await service_delete_diary(diary_url_code)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return {"message":"delete successfully@!@!@!@!@!@!@"}


@diary_router.get("/search", description="날짜 또는 제목으로 다이어리 검색")
async def api_search_diaries(
    title: Optional[str] = None,
    date: Optional[date] = Depends(),
    current_user: Users = Depends() # get_current_user
) -> list[GetDiary]:
    diaries = await service_search_diaries(current_user, title, date)
    return [GetDiary(diary) for diary in diaries]

@diary_router.get("/{tag_name}/diaries", description="태그로 다이어리 검색")
async def api_search_diaries_tag(
    tag_name: str,
    current_user: Users = Depends() # get_current_user
) -> list[GetDiary]:
    diaries = await service_get_diary_by_tag(current_user, tag_name)
    return [GetDiary(diary) for diary in diaries]