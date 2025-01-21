from datetime import datetime, timezone  # Импортируем timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship

from app.db.session import Base  # Импортируем базовый класс из db
from app.db.models.financeModel import Expense, Income  # noqa


# Таблица пользователей, содержит информацию о пользователях системы.
class User(Base):
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
    family = relationship("Family", back_populates="members")
    role = relationship("Role")

    # Связь с расходами и доходами
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")


# Семейная таблица: представляет семейные группы.
class Family(Base):
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
    members = relationship("User", back_populates="family")


# Пример таблицы Role (если её нет, создайте такую)
class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица ролей пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id для каждой роли")
    name = Column(String(20), nullable=False, unique=True, comment="Название роли (например, admin, member)")

#
# class UserView(Base):
#     __tablename__ = 'user_view'
#     __table_args__ = {
#         'schema': 'users',
#         'viewonly': True,
#         'comment': 'Вью пользователей, содержит информацию о пользователях системы'
#     }
#
#     __table__ = Table(
#         'user_view', Base.metadata,
#         Column('id', Integer, primary_key=True, comment="id пользователя"),
#         Column('name', String(100), comment="Имя пользователя"),
#         Column('login', String(255), comment="login"),
#         Column('role_id', Integer, comment="id роли"),
#         Column('role_name', String(20), comment="Роль пользователя"),
#         Column('created_at', DateTime, comment="Дата и время создания пользователя"),
#         Column('family_id', Integer, comment="id семьи"),
#         Column('family_family_name', String(100), comment="Название семьи"),
#         Column('family_description', Text, comment="Описание семьи"),
#         schema='users'
#     )
#
#     # Запрос для определения данных вьюхи
#     query = (
#         select(
#             User.id,
#             User.name,
#             User.login,
#             User.role_id,
#             Role.name.label('role_name'),
#             User.created_at,
#             User.family_id,
#             Family.family_name.label('family_family_name'),
#             Family.description.label('family_description')
#         )
#         .join(Family, User.family_id == Family.id, isouter=True)
#         .join(Role, User.role_id == Role.id, isouter=True)
#     )
