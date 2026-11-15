from __future__ import annotations

import os
from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings configuration.
    Loads from environment variables or .env file with zero-configuration sensible defaults.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "The Royal Banquet Palace API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development | staging | production")
    DEBUG: bool = True

    # Server Binding
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database Configuration (Supports SQLite async out of the box, or PostgreSQL via DATABASE_URL)
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./royal_banquet.db",
        description="Async SQLAlchemy database connection string"
    )

    # Security & JWT Auth
    SECRET_KEY: str = Field(
        default="royal_banquet_super_secure_jwt_secret_key_dwarka_2026_palace",
        description="HMAC secret key for signing admin authentication tokens"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Default Admin Credentials for initial seeding
    DEFAULT_ADMIN_USERNAME: str = "admin@theroyalbanquetpalace.com"
    DEFAULT_ADMIN_PASSWORD: str = "RoyalDwarka2026!"

    # CORS Allow Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]


@lru_cache()
def get_settings() -> Settings:
    """Returns singleton cached settings instance."""
    return Settings()
