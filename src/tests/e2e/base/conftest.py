import pytest


@pytest.fixture()
def health_url() -> str:
    return "public/health"


@pytest.fixture()
def register_url() -> str:
    return "public/auth/register"


@pytest.fixture()
def login_url() -> str:
    return "public/auth/login"
