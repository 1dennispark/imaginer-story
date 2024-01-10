from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
    )

    completion_model: str = 'gpt-3.5-turbo'
    openai_api_key: str
    mysql_url: str