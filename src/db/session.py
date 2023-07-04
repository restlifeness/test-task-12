
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings, PostgresDrivers


settings = get_settings()
DATABASE_URI = settings.get_db_uri(driver=PostgresDrivers.asyncpg)

engine = create_async_engine(DATABASE_URI, future=True)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
