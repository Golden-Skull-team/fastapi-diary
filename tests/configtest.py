import pytest
from tortoise.contrib.test import finalizer, initializer
import sys
import os

@pytest.fixture(scope="function", autouse=True)
def initialize_db():
    initializer(
        ["models.users", "models.diaries", "models.tags"],  # app의 모델 모듈 경로
        db_url="sqlite://:memory:",  # 또는 PostgreSQL 테스트용 URL
        app_label="models"  # Tortoise init에서 지정한 app_label
    )
    yield
    finalizer()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))