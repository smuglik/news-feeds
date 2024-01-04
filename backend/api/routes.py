from fastapi import APIRouter

from api.endpoints import auth, feeds

routes = APIRouter()
routes.include_router(feeds.routes, tags=['feeds'])
routes.include_router(auth.routes, tags=['authentication'])

