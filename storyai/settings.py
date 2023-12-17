from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
    )

    db_path: str = 'storyai.db'
    completion_model: str = 'gpt-3.5-turbo'
    openai_api_key: str