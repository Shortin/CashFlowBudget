from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import Config  # Импортируем строку подключения из config.py

# Инициализация движка подключения
engine = create_engine(Config.SQLALCHEMY_DATABASE_URL)

# Сессия
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
