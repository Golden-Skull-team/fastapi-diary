from fastapi import APIRouter, HTTPException 
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from app.schemas.get_diary_schemas import Diary, Tag, DiaryTag
from app.schemas.create_diary_schemas import CreateDiary
from app.schemas.get_diary_schemas import GetDiary
from app.schemas.update_diary_schemas import (
    UpdateDiaryTitle,
    UpdateDiaryContent,
    UpdateDiaryTag,
    UpdateDiaryMood
)
from app.services.diary_service import (
    service_create_diary,
    service_get_diary,
    service_update_diary_title,
    service_update_diary_content,
    service_update_diary_tag,
    service_update_diary_mood,
    service_delete_diary
)


diary_router = APIRouter(prefix="/diarys", tags=["Diary"])


@diary_router.post("/", description="Diary 생성")
async def api_create_diary() -> CreateDiary:
    return CreateDiary(url_code=(await service_create_diary()).url_code)


@diary_router.get("/{diary_url_code}", description="Diary 조회")
async def api_get_diary(diary_url_code: str) -> GetDiary:
    diary = await service_get_diary(diary_url_code)

    if diary is None: 
        raise HTTPException( 
            status_code=HTTP_404_NOT_FOUND, detail=f"diary with url_code: {diary_url_code} not found"
        )
    return GetDiary(diary)


@diary_router.patch("/{diary_url_code}/title", description="diary title를 수정합니다.")
async def api_update_diary_title(
    diary_url_code: str, update_diary_Title: UpdateDiaryTitle
) -> GetDiary:
    diary = await service_update_diary_title(diary_url_code, update_diary_Title)

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