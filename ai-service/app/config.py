from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/adaptive_learning"
    embedding_model: str = "all-MiniLM-L6-v2"
    ai_service_key: str = "dev-secret-key"
    redis_url: str = "redis://localhost:6379/0"

    # Feature flags for adaptive layers
    enable_bkt: bool = True
    enable_elo: bool = True
    enable_mab: bool = True
    enable_fsrs: bool = True
    enable_llm: bool = False

    # MAB recommendation thresholds
    prereq_mastery_threshold: float = 0.6   # min mastery to unlock dependent concepts
    mastered_threshold: float = 0.95        # concept considered fully mastered

    # LLM configuration (OpenAI-compatible: works with OpenAI, Gemini, etc.)
    openai_api_key: str = ""
    llm_base_url: str = ""  # Override for non-OpenAI providers (e.g. Gemini)
    llm_model: str = "gpt-4o-mini"
    llm_max_tokens: int = 500
    llm_rate_limit_per_minute: int = 30

    # Chatbot configuration
    enable_chatbot: bool = True
    chatbot_max_tokens: int = 800
    chatbot_temperature: float = 0.7
    chatbot_timeout: float = 20.0
    chatbot_rate_limit_per_minute: int = 20

    # Evaluation/experiment settings
    experiment_mode: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()
