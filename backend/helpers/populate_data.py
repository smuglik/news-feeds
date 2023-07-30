import asyncio
import sys

from mimesis import Schema, Field
from mimesis.locales import Locale

from database.models import Product
from database.sessions import SessionLocal


async def main() -> None:
    """
    Generate data in DB
    :return: None
    """
    f = Field(Locale.EN)
    schema = Schema(
        schema=lambda: {
            "name": f("finance.company"),
            "description": f("text.text", quantity=10),
            "cost": f("finance.price", minimum=10, maximum=3000)
        },
        iterations=20
    )
    data = schema.create()
    async with SessionLocal() as session:
        session.add_all([Product(**item) for item in data])
        await session.commit()


if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
