from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/adaptive_learning"
    embedding_model: str = "all-MiniLM-L6-v2"
    ai_service_key: str = "dev-secret-key"

    model_config = {"env_file": ".env"}


settings = Settings()
