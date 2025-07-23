from fastapi import FastAPI
from app.api import auth, user
from contextlib import asynccontextmanager
from app.api.user import router as user_router
from app.api.diarys import diary_router
from app.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(diary_router)
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users")