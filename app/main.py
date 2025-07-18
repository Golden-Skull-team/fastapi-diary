from fastapi import FastAPI
from app.database import init_db, close_db

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db


@app.on_event("shutdown")
async def shutdown_event():
    await close_db
