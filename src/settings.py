from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_base_url: str = "https://openrouter.ai/api/v1"
    openai_model: str = "amazon/nova-2-lite-v1:free"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
