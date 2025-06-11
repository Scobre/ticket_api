from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import Base, engine
from app.routers.ticket import router


def startup(app: FastAPI, engine):
    """This function do some actions in startup of the app.

    :param app: the app of the project
    :param engine: the engine of the database
    :type app: FastAPI

    """
    Base.metadata.create_all(bind=engine)
    app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function do some actions in startup and in shutdown of the app.

    :param app: the app of the project
    :type app: FastAPI

    """
    startup(app, engine)
    yield
