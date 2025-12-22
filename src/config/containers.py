from contextlib import asynccontextmanager
from types import ModuleType
from typing import AsyncGenerator

from dependency_injector import containers, providers

from src.application.use_cases.common.crud import CRUDUseCase
from src.application.use_cases.forms.submit_form import SubmitFormUseCase
from src.config.settings import Settings
from src.infrastructure.managers.amocrm_client import AmoCRMClient
from src.infrastructure.managers.recaptcha_client import RecaptchaClient
from src.infrastructure.managers.unisender_client import UnisenderClient

# from src.infrastructure.managers.jwt_manager import JWTManager
from src.infrastructure.repositories.alchemy.db import Database
from src.infrastructure.uow import SqlAlchemyUnitOfWork, UnitOfWork


class ClientsContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=Settings)

    recaptcha_client = providers.Singleton(
        RecaptchaClient,
        settings=settings,
    )

    unisender_client = providers.Singleton(
        UnisenderClient,
        settings=settings,
    )

    amocrm_client = providers.Factory(
        AmoCRMClient,
        settings=settings,
    )


class DBContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=Settings)

    db: providers.Provider[Database] = providers.Singleton(Database, settings=settings.provided.db)

    uow: providers.Provider[UnitOfWork] = providers.Factory(
        SqlAlchemyUnitOfWork, session_factory=db.provided.session_factory
    )

    session = providers.Factory(lambda db: db.session_factory(), db)


class Container(containers.DeclarativeContainer):
    settings: providers.Provider[Settings] = providers.Singleton(Settings)

    db = providers.Container(DBContainer, settings=settings)

    clients = providers.Container(ClientsContainer, settings=settings)

    # jwt_manager = providers.Singleton(JWTManager, settings=settings)

    ###################
    #### Use cases ####
    ###################

    crud_use_case: providers.Provider[CRUDUseCase] = providers.Factory(
        CRUDUseCase,
        uow=db.container.uow,
    )

    submit_form_use_case = providers.Factory(
        SubmitFormUseCase,
        uow=db.uow,
        recaptcha_client=clients.container.recaptcha_client,
        unisender_client=clients.container.unisender_client,
        amocrm_client=clients.container.amocrm_client,
    )

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, wireable_packages: list[ModuleType]) -> AsyncGenerator["Container", None]:
        container = cls()
        container.wire(packages=wireable_packages)
        yield container
