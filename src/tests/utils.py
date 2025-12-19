from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from config.settings import Settings
from infrastructure.enum import RoleEnum

ALEMBIC_CONFIG_PATH = Path(__file__).parents[2] / "alembic.ini"

POSTGRES_DEFAULT_DB_NAME = "postgres"

CHECK_DATABASE_EXISTS_SQL = text("SELECT 1 FROM pg_database WHERE datname = :name ;")

# Operations on database must be executed without params so use strings
CREATE_DATABASE_SQL = "CREATE DATABASE {};"

DISCONNECT_USERS_SQL = text(
    """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = :name AND pid <> pg_backend_pid() ;
    """
)

# Operations on database must be executed without params so use strings
DROP_DATABASE_SQL = "DROP DATABASE {} ;"

DEFAULT_USER_ID = 1
DEFAULT_USER_EMAIL = "admin@ad.ru"


async def recreate_database(settings: Settings) -> None:
    engine = create_default_database_engine(settings)
    if await check_database_exists(engine, settings):
        await drop_database(settings)
    await create_database(settings, engine)
    await engine.dispose()


async def check_database_exists(engine: AsyncEngine, settings: Settings) -> bool:
    async with engine.connect() as connection:
        result = await connection.execute(CHECK_DATABASE_EXISTS_SQL, {"name": settings.db.name})
        return result.rowcount == 1


async def create_database(settings: Settings, engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.execute(text(CREATE_DATABASE_SQL.format(settings.db.name)))


def apply_migrations(connection: AsyncConnection) -> None:
    config = Config(ALEMBIC_CONFIG_PATH)

    config.set_main_option("script_location", str(Path(__file__).resolve().parents[2] / "migrations"))

    config.attributes["connection"] = connection
    command.upgrade(config, "head")


async def drop_database(settings: Settings) -> None:
    engine = create_default_database_engine(settings)
    async with engine.connect() as connection:
        await connection.execute(DISCONNECT_USERS_SQL, {"name": settings.db.name})
        await connection.execute(text(DROP_DATABASE_SQL.format(settings.db.name)))
    await engine.dispose()


def create_default_database_engine(settings: Settings) -> AsyncEngine:
    default_database_engine = settings.db.model_copy(update={"name": POSTGRES_DEFAULT_DB_NAME})
    return create_async_engine(default_database_engine.dsn, isolation_level="AUTOCOMMIT")


def generate_jwt_token(settings: Settings) -> str:
    payload = {
        "token_type": "access",
        "role": RoleEnum.ADMIN,
        "email": DEFAULT_USER_EMAIL,
        "user_id": DEFAULT_USER_ID,
        "exp": datetime.now(tz=UTC) + timedelta(hours=1),
    }

    return jwt.encode(
        payload,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )
