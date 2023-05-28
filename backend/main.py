from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from api.routes import routes
from settings.base import get_config

conf = get_config()


def create_app() -> FastAPI:
    app = FastAPI(
        title=conf.app_name,
    )
    app.include_router(routes)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    return app


application = create_app()
