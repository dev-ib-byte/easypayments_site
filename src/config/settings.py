from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRECTORY = Path(__file__).parents[2]


class DBSettings(BaseSettings):
    name: str = "easypayments_site"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    dialect: str = "postgresql+asyncpg"
    pool_size: int = 2
    max_overflow: int = 4
    echo: bool = False

    @property
    def dsn(self) -> str:
        print(f"{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}")
        return f"{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseModel):
    title: str = "fastapi-blog-backend"
    debug: bool = False
    version: str = "0.1.0"

    base_url: str = "http://localhost:8002"


class UptraceSettings(BaseModel):
    enabled: bool = False
    dsn: str | None = None


class ApiSettings(BaseModel):
    prefix: str = "/api"
    admin: str = "/admin"
    public: str = "/public"

    docs_endpoint: str = "/docs"
    openapi_endpoint: str = "/openapi.json"

    @property
    def docs_url(self) -> str:
        return f"{self.docs_endpoint}"

    @property
    def openapi_url(self) -> str:
        return f"{self.prefix}{self.openapi_endpoint}"

    @property
    def admin_prefix(self) -> str:
        return f"{self.prefix}{self.admin}"

    @property
    def public_prefix(self) -> str:
        return f"{self.prefix}{self.public}"


class JWTSettings(BaseSettings):
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 600000
    refresh_token_expire_days: int = 600000


class AmoCRMSettings(BaseSettings):
    base_url: str = "https://infoeasypaymentsonline.amocrm.ru"
    client_id: str
    client_secret: str
    redirect_uri: str


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    uptrace: UptraceSettings = UptraceSettings()
    db: DBSettings = DBSettings()
    api: ApiSettings = ApiSettings()
    jwt: JWTSettings = JWTSettings()
    amocrm: AmoCRMSettings = AmoCRMSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )
