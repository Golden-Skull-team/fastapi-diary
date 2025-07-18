# from tortoise.models import Model
import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
