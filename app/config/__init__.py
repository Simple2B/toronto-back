import os
from typing import Any, Dict, List, Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SERVER_NAME: str = "Toronto"
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    JWT_SECRET: str = "secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP: str = "31536000"

    DATA_DIR: str = "data/"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
