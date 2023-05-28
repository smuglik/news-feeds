from fastapi import APIRouter

from api.endpoints import auth, feeds, products

routes = APIRouter()
routes.include_router(feeds.routes, tags=['feeds'])
routes.include_router(auth.routes, tags=['authentication'])
routes.include_router(products.routes, tags=['products'])

