from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Contract Risk Radar"
    API_V1_STR: str = "/api"
    # Set this to the frontend origin in production.
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    JWT_SECRET_KEY: str = "CHANGE_ME_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    FILE_STORAGE_DIR: str = "./storage"
    ENABLE_PERSIST_CONTRACTS: bool = False

    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
    LLM_PROVIDER: str = "groq"  # "groq" or "openai"

    # MongoDB Atlas connection string for users and contracts.
    MONGO_URI: str = "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = "contract_radar"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
