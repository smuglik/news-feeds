import functools

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    debug: bool = Field(default=False)
    port: int = 3456
    app_name: str = "News portal"

    postgres_port: int = Field(env='POSTGRES_PORT')
    postgres_host: str = Field(env='POSTGRES_HOST')
    postgres_user: str = Field(env='POSTGRES_USER')
    postgres_password: SecretStr = Field(env='POSTGRES_PASSWORD')
    postgres_db: str = Field(env='POSTGRES_DB')
    postgres_schema: str = Field(env='POSTGRES_SCHEMA')

    redis_port: int = Field(env='REDIS_PORT')
    redis_host: str = Field(env='REDIS_HOST')
    redis_user: str = Field(env='REDIS_USER')
    redis_password: SecretStr = Field(env='REDIS_PASSWORD')

    auth_token_length: int = 40



@functools.lru_cache
def get_config() -> Settings:
    return Settings()
