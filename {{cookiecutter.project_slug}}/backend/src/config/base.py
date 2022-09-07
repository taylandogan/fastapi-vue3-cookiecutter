import secrets
import pathlib
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from api.utils import get_version


repo_root = pathlib.Path(__file__).parent.parent.parent
version = get_version(repo_root / "REVISION")


class Settings(BaseSettings):
    ENV: str = "test"

    NAME: str = "{{cookiecutter.project_slug}}"
    VERSION: str = version
    HOST: AnyHttpUrl
    PORT: str = 8000
    DEBUG: bool = True
    REPO_ROOT: str
    BASE_PATH: str

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_SSL: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_RECYCLE_TTL: int = 3600
    DATABASE_POOL_MAX_OVERFLOW: int = 1

    SECRET_KEY: str = "{{cookiecutter.secret_key}}"

    # 60 minutes * 24 hours * 1 day = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    CORS_ALLOWED_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]

    @validator("CORS_ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env", ".env.prod"
        env_file_encoding = "utf-8"
        secrets_dir = "/run/secrets"


settings = Settings()
