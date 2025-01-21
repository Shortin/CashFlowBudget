from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import DBConfig  # Импортируем строку подключения из config.py

engine = create_async_engine(DBConfig().get_asyncpg_db_url(), echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Базовый класс для моделей
Base = declarative_base()


@asynccontextmanager
async def get_sessions():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()