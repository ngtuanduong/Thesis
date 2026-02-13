from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pgvector.sqlalchemy import Vector  # noqa: F401 — registers vector type

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
