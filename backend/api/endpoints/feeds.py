from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_post, find_user_by_email
from api.dependencies import get_db_session, get_user_email
from api.schemas import PostIn

routes = APIRouter()


@routes.post("/news/")
async def post_news(
        post: PostIn,
        user_email: EmailStr = Depends(get_user_email),
        db_session: AsyncSession = Depends(get_db_session)
        ):
    user = await find_user_by_email(user_email, db_session)
    post_out = await create_post(post, user, db_session)
    return post_out


async def show_news(

        ):
    pass
