from fastapi import FastAPI

from api.routes import routes
from settings.base import get_config

conf = get_config()


def create_app() -> FastAPI:

    app = FastAPI(
        title=conf.app_name,
        )
    app.include_router(routes)
    return app


app = create_app()

