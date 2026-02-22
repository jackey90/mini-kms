from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    telegram_bot_token: str = ""
    teams_app_id: str = ""
    teams_app_password: str = ""
    intent_confidence_threshold: float = 0.7
    database_url: str = "sqlite:///./data/intelliknow.db"
    data_dir: str = "./data"
    max_file_size_bytes: int = 50 * 1024 * 1024

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
