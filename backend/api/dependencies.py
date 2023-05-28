from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import token_validation_exception
from database.sessions import SessionLocal, redis_connection

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    )


async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_redis_session() -> Redis:
    async with redis_connection as conn:
        yield conn


async def get_user_email(
        token: str = Depends(oauth2_scheme),
        redis_db: Redis = Depends(get_redis_session),
        ) -> EmailStr:
    """
    Return user email related to auth token
    :param token: Dependency return Bearer token
    :param redis_db: dependency return redis session
    :return:
    """
    user = await redis_db.get(token)
    if not user:
        raise token_validation_exception
    return user
