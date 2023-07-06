
from pydantic import BaseSettings


class PostgresDrivers:
    asyncpg = "asyncpg"
    psycopg2 = "psycopg2"


class ProjectSettings(BaseSettings):
    APP_NAME: str = "FastAPI Blog"

    DEBUG: bool = True

    HOST: str = "localhost"
    PORT: int = 8000

    POST_LIKES_CACHE_THRESHOLD: int = 100

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"

    def get_db_uri(self, driver: str) -> str:
        return f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"\
            + f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_redis_uri(self, database: int = 0) -> str:
        return f"redis://{self.REDIS_HOST}/{database}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> ProjectSettings:
    return ProjectSettings()
