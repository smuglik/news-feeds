from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserIn
from database.models import User

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
