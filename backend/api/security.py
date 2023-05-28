from secrets import token_hex

from passlib.context import CryptContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import find_user_by_email
from api.exceptions import credentials_validation_exception
from api.schemas import Credentials
from settings.base import get_config

conf = get_config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token() -> str:
    return token_hex(conf.auth_token_length)


# TODO add password hasher
async def login(
        credentials: Credentials,
        db_session: AsyncSession,
        redis_session: Redis,
        ) -> str:
    user = await find_user_by_email(
        credentials.email,
        db_session,
        )
    if not user.password == credentials.password.get_secret_value():
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
