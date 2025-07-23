import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
ENV_PATH = Path(".") / (".env.prod" if os.getenv("APP_ENV") == "production" else ".env")
load_dotenv(dotenv_path=ENV_PATH)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

settings = Settings()
