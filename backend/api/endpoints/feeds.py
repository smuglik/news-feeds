from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_post, find_user_by_email, get_posts
from api.dependencies import get_db_session, get_user, get_user_email
from api.schemas import PostIn, PostOut
from database.models import User


routes = APIRouter()


@routes.post("/news/")
async def post_news(
        post: PostIn,
        user_email: Annotated[EmailStr, Depends(get_user_email)],
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> PostOut:
    user = await find_user_by_email(user_email, db_session)
    post_out = await create_post(post, user, db_session)
    return post_out


@routes.get("/news/")
async def show_news(
        user: Annotated[User, Depends(get_user)],
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> list[PostOut]:
    posts = await get_posts(session=db_session, user=user)
    return posts
