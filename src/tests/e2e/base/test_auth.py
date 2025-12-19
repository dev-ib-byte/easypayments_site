import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "params",
    [
        {
            "first_name": "Тест",
            "last_name": "Тесов",
            "email": "test@test.com",
            "password": "test",
        }
    ],
)
async def test_registration(http_client: AsyncClient, register_url: str, params: dict) -> None:
    response = await http_client.post(register_url, params=params)

    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user_id" in data


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "first_name": "Тест",
            "last_name": "Тесов",
            "email": "test@test.com",
            "password": "test",
        }
    ],
)
async def test_login_success(
    http_client: AsyncClient, register_url: str, login_url: str, user_data: dict
) -> None:
    reg_response = await http_client.post(register_url, params=user_data)
    assert reg_response.status_code == status.HTTP_200_OK, reg_response.text

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"],
    }
    login_response = await http_client.post(login_url, params=login_data)

    assert login_response.status_code == status.HTTP_200_OK, login_response.text
    data = login_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user_id" in data


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "params",
    [
        {"email": "notexists@test.com", "password": "test"},
    ],
)
async def test_login_user_does_not_exist(http_client: AsyncClient, login_url: str, params: dict) -> None:
    response = await http_client.post(login_url, params=params)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio(loop_scope="session")
async def test_login_wrong_password(http_client: AsyncClient, register_url: str, login_url: str) -> None:
    user = {
        "first_name": "Тест",
        "last_name": "Тесов",
        "email": "wrong@test.com",
        "password": "correct",
    }
    reg_response = await http_client.post(register_url, params=user)
    assert reg_response.status_code == status.HTTP_200_OK

    wrong_login = {"email": user["email"], "password": "incorrect"}
    login_response = await http_client.post(login_url, params=wrong_login)

    assert login_response.status_code == status.HTTP_400_BAD_REQUEST
