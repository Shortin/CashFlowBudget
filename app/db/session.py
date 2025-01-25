from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import DBConfig

engine = create_async_engine(DBConfig().get_asyncpg_db_url(), echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

@asynccontextmanager
async def get_sessions():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
