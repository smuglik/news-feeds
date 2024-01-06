from pydantic import EmailStr
from sqlalchemy import func, label, select
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
    obj = await session.execute(
        select(
            Post.id,
            Post.created,
            Post.title,
            Post.body,
            label(
                "author", func.concat(
                    User.first_name, " ", User.last_name, "<", User.email, ">"
                )
            )
        ).where(Post.id == db_post.id).join(User, Post.author_id == User.id)
    )
    return PostOut.model_validate(*obj.all())  # not quite safe


async def get_posts(
        user: User,
        session: AsyncSession
) -> list[Post]:
    posts = await session.execute(
        select(
            Post.id,
            Post.created,
            Post.title,
            Post.body,
            label(
                "author", func.concat(
                    User.first_name, " ", User.last_name, "<", User.email, ">"
                )
            )
        ).where(Post.author_id == user.id).join(User, Post.author_id == User.id)
    )
    return posts.fetchall()
