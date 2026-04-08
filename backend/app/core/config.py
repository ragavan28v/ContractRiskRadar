import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Contract Risk Radar"
    API_V1_STR: str = "/api"
    # When developing locally, '*' is acceptable; tighten in production.
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "contract_user"
    POSTGRES_PASSWORD: str = "contract_pass"
    POSTGRES_DB: str = "contract_radar"

    JWT_SECRET_KEY: str = "CHANGE_ME_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    FILE_STORAGE_DIR: str = "./storage"
    ENABLE_PERSIST_CONTRACTS: bool = False

    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
    LLM_PROVIDER: str = "groq"  # "groq" or "openai"

    # MongoDB connection string for storing consented contracts
    MONGO_URI: str = "mongodb://localhost:27017/"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
