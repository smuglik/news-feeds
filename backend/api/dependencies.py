from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from api.crud import find_user_by_email
from api.exceptions import token_validation_exception
from database.models import User
from database.sessions import SessionLocal, redis_connection

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)
logger = get_logger()


async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_redis_session() -> Redis:
    async with redis_connection as conn:
        yield conn


async def get_user_email(
        token: str = Depends(oauth2_scheme),
        redis_db: Redis = Depends(get_redis_session),
) -> str:
    """
    Return user email related to auth token
    :param token: Dependency return Bearer token
    :param redis_db: dependency return redis session
    :return:
    """
    user_email = await redis_db.get(token)
    if not user_email:
        raise token_validation_exception
    return user_email.decode("utf-8")


async def get_user(
        user_email: Annotated[EmailStr, Depends(get_user_email)],
        db: Annotated[AsyncSession, Depends(get_db_session)]
) -> User:
    user = await find_user_by_email(user_email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with such email does not exists"
        )
    return user
