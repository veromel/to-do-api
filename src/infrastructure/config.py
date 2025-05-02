from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación.
    """

    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "To-do API"

    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./todo_api.db"
    DB_ECHO: bool = False

    # Security settings
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = "TODO_"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
