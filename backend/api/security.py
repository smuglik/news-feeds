from secrets import token_hex

import argon2
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from api.crud import find_user_by_email
from api.exceptions import credentials_validation_exception
from api.schemas import Credentials
from settings.base import get_config


conf = get_config()

ph = PasswordHasher()
logger = get_logger()


def generate_token() -> str:
    return token_hex(conf.auth_token_length)


def get_hashed_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        logger.debug("Password does not match")
    except argon2.exceptions.VerificationError as e:
        logger.error("During password verification an exception occurred")
        logger.error(e)
    except argon2.exceptions.InvalidHashError as e:
        logger.error("Invalid hash for verification")
        logger.error(e)
    return False


async def login(
        credentials: Credentials,
        db_session: AsyncSession,
        redis_session: Redis,
) -> str:
    user = await find_user_by_email(
        credentials.email,
        db_session,
    )
    if not verify_password(credentials.password.get_secret_value(), user.password):
        raise credentials_validation_exception
    t = generate_token()
    await redis_session.set(
        name=t,
        value=user.email,
        ex=3600
    )
    return t


async def logout(
        redis_session: Redis,
        token: str,
) -> bool:
    await redis_session.delete(token)
    return True
