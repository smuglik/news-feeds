import functools

from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    port: int = 3456
    app_name = "News portal"

    pg_port: int = Field(env='postgres_port')
    pg_host: str = Field(env='postgres_host')
    pg_user: str = Field(env='postgres_user')
    pg_password: SecretStr = Field(env='postgres_password')
    pg_db: str = Field(env='postgres_db')
    pg_schema: str = Field(env='postgres_schema')

    redis_port: int = Field(env='redis_port')
    redis_host: str = Field(env='redis_host')
    redis_user: str = Field(env='redis_user')
    redis_password: SecretStr = Field(env='redis_password')

    auth_token_length: int = 40

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@functools.lru_cache
def get_config() -> Settings:
    return Settings()
