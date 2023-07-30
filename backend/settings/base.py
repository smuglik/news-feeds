import functools

from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    port: int = 3456
    app_name = "News portal"

    pg_port: int = Field(env='POSTGRES_PORT')
    pg_host: str = Field(env='POSTGRES_HOST')
    pg_user: str = Field(env='POSTGRES_USER')
    pg_password: SecretStr = Field(env='POSTGRES_PASSWORD')
    pg_db: str = Field(env='POSTGRES_DB')
    pg_schema: str = Field(env='POSTGRES_SCHEMA')

    redis_port: int = Field(env='REDIS_PORT')
    redis_host: str = Field(env='REDIS_HOST')
    redis_user: str = Field(env='REDIS_USER')
    redis_password: SecretStr = Field(env='REDIS_PASSWORD')

    auth_token_length: int = 40

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


@functools.lru_cache
def get_config() -> Settings:
    return Settings()
