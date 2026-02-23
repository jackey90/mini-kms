from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    telegram_bot_token: str = ""
    teams_app_id: str = ""
    teams_app_password: str = ""
    intent_confidence_threshold: float = 0.7
    conversation_history_limit: int = 5  # number of recent Q&A pairs to include as context
    database_url: str = "sqlite:///./data/intelliknow.db"
    data_dir: str = "./data"
    max_file_size_bytes: int = 50 * 1024 * 1024

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
