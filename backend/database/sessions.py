import redis.asyncio as redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings.base import get_config

conf = get_config()

POSTGRES_URL = "postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}".format(
    user=conf.postgres_user,
    password=conf.postgres_password.get_secret_value(),
    host=conf.postgres_host,
    port=conf.postgres_port,
    db_name=conf.postgres_db,
)

engine = create_async_engine(POSTGRES_URL, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

redis_connection = redis.Redis(
    host=conf.redis_host,
    port=conf.redis_port,
    username=conf.redis_user,
    password=conf.redis_password.get_secret_value(),
    # decode_responses=True,
    db=0,
)
