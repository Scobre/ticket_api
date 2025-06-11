from functools import lru_cache

from dotenv import load_dotenv
from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings

from app.enums.environment import EnvironmentEnum

load_dotenv()


class _Settings(BaseSettings):
    app_version: str = "0.0.1"
    database_engine: str = "sqlite"
    database_url: str = "sqlite:///./db/sql_app.db"
    fastapi_env: EnvironmentEnum = EnvironmentEnum.dev
    fastapi_title: str = "Ticket - API"

    model_config = ConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings() -> _Settings:
    """This function get the setting of the app.

    :returns: _Settings

    """
    return _Settings()


settings = get_settings()
