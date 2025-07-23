from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user
from contextlib import asynccontextmanager
from app.api.user import router as user_router
from app.api.diarys import diary_router
from app.api.ai import router as ai_router
from app.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-domain.com"],  # 실제 배포 프론트 도메인으로 교체
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router)
app.include_router(diary_router)
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users")
app.include_router(ai_router)