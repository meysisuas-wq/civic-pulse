from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import structlog
from src.config import settings

logger = structlog.get_logger()
convention = {"ix": "ix_%(column_0_label)s", "uq": "uq_%(table_name)s_%(column_0_name)s",
              "ck": "ck_%(table_name)s_%(constraint_name)s", "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
              "pk": "pk_%(table_name)s"}
metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    metadata = metadata

engine = create_async_engine(settings.DATABASE_URL, pool_size=settings.DATABASE_POOL_SIZE, echo=settings.APP_DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    logger.info("Initializing database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")

async def close_db():
    await engine.dispose()
    logger.info("Database closed")
