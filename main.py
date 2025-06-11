from fastapi import FastAPI

from app.config.env import settings
from app.config.lifespan import lifespan

app = FastAPI(
    # use the env ROOT_PATH to define the root url
    lifespan=lifespan,
    title=settings.fastapi_title,
    version=settings.app_version,
)
