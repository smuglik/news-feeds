from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import PostIn, PostOut, UserIn, Product as ProductSchema
from database.models import Post, User, Product
from database.sessions import redis_connection


async def create_user_in_db(
        user: UserIn,
        session: AsyncSession,
) -> User:
    db_user = User(
        **user.dict(),
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
        **post.dict(),
        author=user
    )
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return PostOut.from_orm(db_post)


async def get_posts(
        session: AsyncSession
):
    posts = await session.scalars(
        select(Post)
    )


async def get_products(session: AsyncSession) -> list[Product]:
    """
    Return hole list of Products
    :param session:
    :return:
    """
    products = await session.scalars(select(Product))
    res = []

    for product in products:
        async with redis_connection as conn:
            image = await conn.get(product.image_id)
            t = ProductSchema.from_orm(product)
            t.image = image
            res.append(t)

    return res
