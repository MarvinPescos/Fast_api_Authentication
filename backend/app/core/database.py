from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from typing import AsyncGenerator
import logging

from app.core import settings
from app.errors import DatabaseConnectionError

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            logger.info("Attempting to connect to database")
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database Connection error: {str(e)}")
            raise DatabaseConnectionError(f"Database connection failed: {str(e)}")
        except Exception as e:
            # Re-raise other exception like HTTPException
            raise
        finally:
            await session.close()

