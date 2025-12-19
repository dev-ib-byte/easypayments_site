import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_health_app_is_alive(http_client: AsyncClient, health_url: str) -> None:
    response = await http_client.get(health_url)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }
