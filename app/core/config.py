from dotenv import load_dotenv
import os
from pathlib import Path

# .env 파일 로드
ENV_PATH = Path('.') / ('.env.prod' if os.getenv("APP_ENV") == "production" else '.env')
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()