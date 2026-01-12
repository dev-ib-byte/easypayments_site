import httpx
from fastapi import HTTPException, status

from src.api.schemas import AccessTokenResponseSchema


class AuthServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def validate_access_token(self, token: str) -> AccessTokenResponseSchema:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                f"{self._base_url}/v1/auth/validate-access-token",
                json={"access_token": token},
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired access token",
            )

        return AccessTokenResponseSchema.model_validate(response.json())
