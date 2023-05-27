from fastapi import FastAPI
from loguru import logger
import uvicorn

from settings.base import get_config

conf = get_config()

app = FastAPI(title=conf.app_name)

if __name__ == '__main__':
    logger.info("Starting of Application")
    uvicorn.run(
        app=app,
        port=conf.port,
    )
