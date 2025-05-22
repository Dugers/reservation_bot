from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from reservation_bot.config import settings

engine = create_async_engine(settings.mysql.url)
session_maker = async_sessionmaker(engine)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()