
from pydantic import BaseSettings


class PostgresDrivers:
    asyncpg = "asyncpg"
    psycopg2 = "psycopg2"


class ProjectSettings(BaseSettings):
    APP_NAME: str = "FastAPI Blog"

    DEBUG: bool = True

    HOST: str = "localhost"
    PORT: int = 8000

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"

    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"

    def get_db_uri(self, driver: str) -> str:
        return f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"\
            + f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> ProjectSettings:
    return ProjectSettings()
