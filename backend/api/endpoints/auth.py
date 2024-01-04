from fastapi import APIRouter, Depends, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from api.crud import create_user_in_db, find_user_by_email
from api.dependencies import get_db_session, get_redis_session, get_user_email, oauth2_scheme
from api.schemas import Credentials, UserIn, UserOut
from api.security import login, logout
from database.models import User

routes = APIRouter()
logger = get_logger()


@routes.post("/users/")
async def create_user(
        user: UserIn,
        db_session: AsyncSession = Depends(get_db_session),
) -> UserOut:
    logger.debug(f"{user=}")
    created_user = await create_user_in_db(user, session=db_session)
    return UserOut.from_orm(created_user)


@routes.get("/user-info/")
async def user_info(
        email: User = Depends(get_user_email),
        db_session: AsyncSession = Depends(get_db_session),
) -> UserOut:
    user = await find_user_by_email(email=email, session=db_session)
    return user


@routes.post("/auth/")
async def authenticate_user(
        cred: Credentials,
        db_session: AsyncSession = Depends(get_db_session),
        redis_session: Redis = Depends(get_redis_session),
) -> dict[str, str]:
    token = await login(cred, db_session, redis_session)
    return {"token": token}


@routes.post("/logout/")
async def logout_user(
        token: str = Depends(oauth2_scheme),
        redis_session: Redis = Depends(get_redis_session),
) -> Response:
    await logout(redis_session, token)
    return Response(status_code=204)
