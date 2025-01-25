from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.models.financeModel import MTransaction  # noqa
from app.db.session import Base


class MUser(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица пользователей, содержит информацию о пользователях системы'
    }

    id = Column(Integer, primary_key=True, comment="id для каждого пользователя")
    name = Column(String(100), nullable=False, comment="Имя пользователя")
    birthday = Column(Date, comment="Дата рождения")
    role_id = Column(Integer, ForeignKey('data.role.id'), nullable=False, comment="Ссылка на роль пользователя")
    username = Column(String(255), unique=True, nullable=False, comment="Уникальный username для входа в систему")
    telegram_chat_id = Column(Integer, unique=True, nullable=True,
                              comment="Идентификатор телеграм чата данного пользователя")
    password_hash = Column(String(255), nullable=False, comment="Хэш пароля для аутентификации")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        comment="Дата и время создания записи пользователя")

    role = relationship("MRole", lazy="joined")
    expenses = relationship("MTransaction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MUser(id={self.id}, name={self.name}, username={self.username}, role_id={self.role_id}, " \
               f"telegram_chat_id={self.telegram_chat_id}, created_at={self.created_at})>"


class MRole(Base):
    __tablename__ = 'role'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица ролей пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id для каждой роли")
    name = Column(String(20), nullable=False, unique=True, comment="Название роли (например, admin, member)")

    def __repr__(self):
        return f"<MRole(id={self.id}, name={self.name})>"

    class RoleName(str, Enum):
        admin = 'admin'
        user = 'user'
