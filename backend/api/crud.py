from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import PostIn, PostOut, UserIn
from database.models import Post, User


async def create_user_in_db(
        user: UserIn,
        session: AsyncSession,
) -> User:
    db_user = User(
        **user.model_dump(),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def find_user_by_email(
        email: EmailStr,
        session: AsyncSession,
) -> User | None:
    user = await session.scalar(
        select(User).where(User.email.ilike(email)),
    )
    return user


async def create_post(
        post: PostIn,
        user: User,
        session: AsyncSession
) -> PostOut:
    db_post = Post(
        **post.model_dump(),
        author=user
    )
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return PostOut.model_validate(db_post, from_attributes=True)


async def get_posts(
        user: User,
        session: AsyncSession
):
    posts = await session.execute(
        select(Post).where(Post.author_id == user.id)
    )
    return posts
