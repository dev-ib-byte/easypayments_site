import pytest

from application.use_cases.common.create import ModelObjectCreateUseCase
from application.use_cases.common.delete import ModelObjectDeleteUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.common.retrieve import ModelObjectRetrieveUseCase
from config.containers import Container


@pytest.fixture(scope="function")
def object_create_use_case(
    container: Container,
) -> ModelObjectCreateUseCase:
    return container.object_create_use_case()


@pytest.fixture(scope="function")
def object_delete_use_case(
    container: Container,
) -> ModelObjectDeleteUseCase:
    return container.object_delete_use_case()


@pytest.fixture(scope="function")
def object_retrieve_use_case(
    container: Container,
) -> ModelObjectRetrieveUseCase:
    return container.object_retrieve_use_case()


@pytest.fixture(scope="function")
def object_list_use_case(
    container: Container,
) -> ModelObjectListUseCase:
    return container.object_list_use_case()
