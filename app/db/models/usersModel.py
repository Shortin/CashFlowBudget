from datetime import datetime, timezone  # Импортируем timezone
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship

from app.db.models.financeModel import MExpense, MIncome  # noqa
from app.db.session import Base  # Импортируем базовый класс из db


# Таблица пользователей, содержит информацию о пользователях системы.
class MUser(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица пользователей, содержит информацию о пользователях системы'
    }

    id = Column(Integer, primary_key=True, comment="id для каждого пользователя")
    name = Column(String(100), nullable=False, comment="Имя пользователя")
    birthday = Column(Date, comment="Дата рождения")
    family_id = Column(Integer, ForeignKey('data.families.id'), nullable=True,
                       comment="Ссылка на семейство (если имеется)")

    role_id = Column(Integer, ForeignKey('data.role.id'), nullable=False, comment="Ссылка на роль пользователя")
    username = Column(String(255), unique=True, nullable=False, comment="Уникальный username для входа в систему")
    telegram_chat_id = Column(Integer, unique=True, nullable=True, comment="Идентификатор телеграм чата данного пользователя" )
    password_hash = Column(String(255), nullable=False, comment="Хэш пароля для аутентификации")

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        comment="Дата и время создания записи пользователя")

    # Связь с таблицей семей (Family)
    family = relationship("MFamily", backref="users", uselist=False, lazy="subquery", passive_deletes=True)
    role = relationship("MRole", lazy="joined")

    # Связь с расходами и доходами
    expenses = relationship("MExpense", back_populates="user", cascade="all, delete-orphan")
    incomes = relationship("MIncome", back_populates="user", cascade="all, delete-orphan")


# Семейная таблица: представляет семейные группы.
class MFamily(Base):
    __tablename__ = 'families'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Семейная таблица: представляет семейные группы'
    }

    id = Column(Integer, primary_key=True, comment="id для каждой семьи")
    family_name = Column(String(100), nullable=False, comment="Название семьи")
    description = Column(Text, nullable=True, comment="Дополнительная информация о семье")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), comment="Дата и время создания записи о семье")

    # Добавим members для связи с User
    user = relationship("MUser", back_populates="family")


# Пример таблицы Role (если её нет, создайте такую)
class MRole(Base):
    __tablename__ = 'role'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица ролей пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id для каждой роли")
    name = Column(String(20), nullable=False, unique=True, comment="Название роли (например, admin, member)")

    class RoleName(str, Enum):
        admin = 'admin'
        user = 'user'
        moderator = 'child'
