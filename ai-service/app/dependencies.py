from collections.abc import AsyncGenerator

from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session


async def verify_service_key(x_service_key: str = Header(...)) -> str:
    if x_service_key != settings.ai_service_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service key",
        )
    return x_service_key


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
