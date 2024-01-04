import asyncio
import sys

from mimesis import Schema, Field
from mimesis.locales import Locale

from api.security import get_hashed_password
from database.models import User
from database.sessions import SessionLocal


async def main() -> None:
    """
    Generate data in DB
    :return: None
    """
    f = Field(Locale.EN)
    schema = Schema(
        schema=lambda: {
            "id": f("uuid"),
            "first_name": f("person.first_name"),
            "last_name": f("person.last_name"),
            "email": f("person.email"),
            "is_superuser": f("boolean"),
            "password": get_hashed_password("1")
        },
        iterations=3
    )
    data = schema.create()
    async with SessionLocal() as session:
        session.add_all([User(**item) for item in data])
        await session.commit()


if __name__ == '__main__':

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
