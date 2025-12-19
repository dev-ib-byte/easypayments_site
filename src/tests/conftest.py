import asyncio
import sys
from asyncio import AbstractEventLoop
from pathlib import Path
from typing import Any, AsyncGenerator, Generator

import pytest
from dependency_injector import providers
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import api
from config.app_factory import create_app
from config.containers import Container
from config.settings import Settings
from infrastructure.repositories.alchemy.db import Database
from infrastructure.uow.alchemy import SqlAlchemyUnitOfWork
from tests.utils import (
    apply_migrations,
    drop_database,
    generate_jwt_token,
    recreate_database,
)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, Any, Any]:
    """
    Fixture for setting up an event loop.
    it must be used when building an application to avoid running tests in different event loops
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = Settings()

    return settings.model_copy(
        update={
            "db": settings.db.model_copy(
                update={
                    "name": f"test_db",
                },
            ),
        }
    )


@pytest.fixture(scope="session")
async def database(settings: Settings, event_loop: AbstractEventLoop) -> AsyncGenerator[None, Any]:
    await recreate_database(settings)

    # Apply migrations to test database
    engine = create_async_engine(settings.db.dsn, poolclass=NullPool)
    async with engine.begin() as connection:
        await connection.run_sync(apply_migrations)
    await engine.dispose()

    try:
        yield
    finally:
        await drop_database(settings)


@pytest.fixture(scope="session")
def alchemy_database(settings: Settings, database: None) -> Database:
    return Database(settings.db)


@pytest.fixture(scope="session")
async def alchemy_engine(
    alchemy_database: Database,
) -> AsyncGenerator[AsyncEngine, Any]:
    yield alchemy_database.engine
    await alchemy_database.engine.dispose()


@pytest.fixture(scope="function")
async def alchemy_session_factory(
    alchemy_engine: AsyncEngine,
    alchemy_database: Database,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], Any]:
    async with alchemy_engine.connect() as connection:
        async with connection.begin() as transaction:
            yield async_sessionmaker(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )
            await transaction.rollback()


@pytest.fixture(scope="function")
async def alchemy_session(
    alchemy_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, Any]:
    async with alchemy_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def container(
    settings: Settings,
    alchemy_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[Container, Any]:
    async with Container.lifespan(
        wireable_packages=[
            api,
            api.public,
            api.admin,
        ]
    ) as container:
        container.settings.override(providers.Singleton(lambda: settings))

        container.db.uow.override(
            providers.Factory(SqlAlchemyUnitOfWork, session_factory=alchemy_session_factory)
        )

        yield container


@pytest.fixture(scope="function")
def app(
    settings: Settings, container: Container, event_loop: AbstractEventLoop
) -> Generator[FastAPI, Any, Any]:
    app = create_app(settings)
    app.container = container
    yield app


@pytest.fixture(scope="session")
def http_client_base_url(settings: Settings) -> str:
    return f"http://test{settings.api.prefix}"


@pytest.fixture(scope="function")
async def http_client(app: FastAPI, http_client_base_url: str) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=http_client_base_url) as client:
        yield client


@pytest.fixture(scope="function")
async def auth_http_client(
    app: FastAPI, http_client_base_url: str, settings: Settings
) -> AsyncGenerator[AsyncClient, Any]:
    token = generate_jwt_token(settings)
    headers = {
        "Authorization": f"Bearer {token}",
    }

    async with AsyncClient(app=app, base_url=http_client_base_url, headers=headers) as client:
        yield client
