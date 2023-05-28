from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import get_products
from api.dependencies import get_db_session
from api.schemas import Product
routes = APIRouter()


@routes.get("/products/")
async def products_list(session: AsyncSession = Depends(get_db_session)) -> list[Product]:
    products = await get_products(session)
    return products
