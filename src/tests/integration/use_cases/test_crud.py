import pytest

from application.use_cases.common.create import ModelObjectCreateUseCase
from application.use_cases.common.delete import ModelObjectDeleteUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.common.retrieve import ModelObjectRetrieveUseCase
from tests.integration.use_cases.params import TEST_CASES


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "model_type, dto_cls, dto_data, entity_cls, read_cls, expected",
    TEST_CASES,
)
async def test_create(
    object_create_use_case: ModelObjectCreateUseCase,
    model_type,
    dto_cls,
    dto_data,
    entity_cls,
    read_cls,
    expected,
) -> None:
    dto = dto_cls(**dto_data)
    result = await object_create_use_case.execute(
        model_type,
        dto,
        entity_cls,
        read_cls,
    )
    assert result.name == expected.name


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "model_type, dto_cls, dto_data, entity_cls, read_cls, expected",
    TEST_CASES,
)
async def test_delete(
    object_create_use_case: ModelObjectCreateUseCase,
    object_delete_use_case: ModelObjectDeleteUseCase,
    object_retrieve_use_case: ModelObjectRetrieveUseCase,
    object_list_use_case: ModelObjectListUseCase,
    model_type,
    dto_cls,
    dto_data,
    entity_cls,
    read_cls,
    expected,
) -> None:
    dto = dto_cls(**dto_data)
    result = await object_create_use_case.execute(
        model_type,
        dto,
        entity_cls,
        read_cls,
    )
    assert result.name == expected.name

    result = await object_retrieve_use_case.execute(result.id, model_type, read_cls)
    assert result.name == expected.name

    await object_delete_use_case.execute(result.id, model_type)
