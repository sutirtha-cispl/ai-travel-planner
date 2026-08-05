"""Centralized application configuration.

Loads environment variables from the project root `.env` file.
Never hardcode API keys, database credentials, or model configuration.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config/settings.py -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Travel Planner API"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./travel.db"

    LLM_PROVIDER: str = "openai"
    MODEL_NAME: str = "gpt-4.1-mini"
    OPENAI_API_KEY: str = ""

    CORS_ORIGINS: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
