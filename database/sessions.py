import redis.asyncio as redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings.base import get_config

conf = get_config()

POSTGRES_URL = "postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}".format(
    user=conf.pg_user,
    password=conf.pg_password.get_secret_value(),
    host=conf.pg_host,
    port=conf.pg_port,
    db_name=conf.pg_db,
    )

engine = create_async_engine(POSTGRES_URL, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

redis_connection = redis.Redis(
    host=conf.redis_host,
    port=conf.redis_port,
    username=conf.redis_user,
    password=conf.redis_password.get_secret_value(),
    decode_responses=True,
    db=0,
    )
