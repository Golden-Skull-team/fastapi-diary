from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tags" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "nickname" VARCHAR(30) NOT NULL,
    "username" VARCHAR(30) NOT NULL,
    "phone_number" VARCHAR(15) NOT NULL,
    "last_login" TIMESTAMPTZ,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "is_admin" BOOL NOT NULL DEFAULT False,
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE TABLE IF NOT EXISTS "diaries" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "mood" VARCHAR(9) NOT NULL,
    "ai_summary" TEXT,
    "url_code" VARCHAR(255) NOT NULL UNIQUE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "diaries"."mood" IS 'glad: glad\nsad: sad\nangry: angry\ntired: tired\nannoyance: annoyance\nsoso: soso';
CREATE TABLE IF NOT EXISTS "diary_tags" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "diary_id" BIGINT NOT NULL REFERENCES "diaries" ("id") ON DELETE CASCADE,
    "tag_id" BIGINT NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_diary_tags_diary_i_cf5d22" UNIQUE ("diary_id", "tag_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "models.DiaryTags" (
    "diaries_id" BIGINT NOT NULL REFERENCES "diaries" ("id") ON DELETE CASCADE,
    "tags_id" BIGINT NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_models.Diar_diaries_1c4693" ON "models.DiaryTags" ("diaries_id", "tags_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
