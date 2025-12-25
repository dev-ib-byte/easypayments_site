from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, Request, status

from src.api.schemas import AccessTokenResponseSchema
from src.config.settings import Settings
from src.infrastructure.managers.auth_client import AuthServiceClient

settings = Settings()
auth_client = AuthServiceClient(settings.api.auth_service_url)


def requires_authentication(*, is_admin: bool = False) -> Callable:
    """
    Универсальный auth-декоратор

    :param is_admin: требует ли admin-доступ
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            request = _extract_request(args, kwargs)

            token = _extract_bearer_token(request)

            auth_user: AccessTokenResponseSchema = await auth_client.validate_access_token(token)

            if not auth_user.verify:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token is not verified",
                )

            if is_admin and auth_user.user_type != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin access required",
                )

            # kwargs["auth_user"] = auth_user
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def _extract_request(args, kwargs) -> Request:
    request = kwargs.get("request")
    if isinstance(request, Request):
        return request

    for arg in args:
        if isinstance(arg, Request):
            return arg

    raise RuntimeError("Request object not found. " "Add `request: Request` to endpoint signature.")


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
        )

    return auth_header.removeprefix("Bearer ").strip()
