import os
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal[
    "development",
    "testing",
    "production",
]


def get_env_file() -> str:
    environment = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    env_files = {
        "development": ".env.dev",
        "testing": ".env.test",
        "production": ".env.prod",
    }

    return env_files.get(
        environment,
        ".env.dev",
    )


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: Environment

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    PASSWORD_RESET_MINUTES: int = 15

    MAX_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCK_MINUTES: int = 15

    JWT_SECRET_KEY: str
    ENCRYPTION_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("DB_PORT")
    @classmethod
    def validate_db_port(cls, value: int) -> int:
        if not 1 <= value <= 65535:
            raise ValueError(
                "DB_PORT must be between 1 and 65535"
            )

        return value

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()
