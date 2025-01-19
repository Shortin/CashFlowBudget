from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Double
from sqlalchemy.orm import relationship

from app.db import Base  # Импортируем базовый класс из db/__init__.py


# Таблица расходов, представляет расходы пользователей.
class Expense(Base):
    __tablename__ = 'expenses'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица расходов, представляет расходы пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id")
    amount = Column(Double, nullable=False, comment="Сумма расхода")
    description = Column(Text, nullable=True, comment="Описание расхода")
    user_id = Column(Integer, ForeignKey('data.users.id'), nullable=False,
                     comment="Ссылка на пользователя, который сделал расход")
    created_at = Column(DateTime, default=datetime.now(timezone.utc), comment="Дата и время создания записи расхода")

    # Связь с таблицей пользователей (User)
    user = relationship("User", back_populates="expenses")


# Таблица доходов, представляет доходы пользователей.
class Income(Base):
    __tablename__ = 'incomes'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Таблица доходов, представляет доходы пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id")
    amount = Column(Double, nullable=False, comment="Сумма дохода")
    description = Column(Text, nullable=True, comment="Описание дохода")
    user_id = Column(Integer, ForeignKey('data.users.id'), nullable=False,
                     comment="Ссылка на пользователя, который сделал доход")
    created_at = Column(DateTime, default=datetime.now(timezone.utc), comment="Дата и время создания записи дохода")

    # Связь с таблицей пользователей (User)
    user = relationship("User", back_populates="incomes")
#
#
#
# # Вьюха для таблицы расходов
# class ExpenseView(Base):
#     __tablename__ = 'expense_view'
#     __table_args__ = {
#         'schema': 'budget',  # Вьюхи обычно располагаются в другой схеме, например, 'budget'
#         'viewonly': True,
#         'comment': 'Вью для таблицы расходов, объединяющая информацию о пользователях и расходах'
#     }
#
#     __table__ = Table(
#         'expense_view', Base.metadata,
#         Column('id', Integer, primary_key=True, comment="id расхода"),
#         Column('amount', Double, comment="Сумма расхода"),
#         Column('description', Text, comment="Описание расхода"),
#         Column('user_id', Integer, comment="id пользователя"),
#         Column('user_name', String(100), comment="Имя пользователя"),
#         Column('created_at', DateTime, comment="Дата и время создания расхода"),
#         schema='budget'
#     )
#
#     # Запрос для определения данных вьюхи
#     query = (
#         select(
#             Expense.id,
#             Expense.amount,
#             Expense.description,
#             Expense.user_id,
#             User.name.label('user_name'),
#             Expense.created_at
#         )
#         .join(User, Expense.user_id == User.id, isouter=True)  # Левое соединение для пользователей без расходов
#     )
#
#
# # Вьюха для таблицы доходов
# class IncomeView(Base):
#     __tablename__ = 'income_view'
#     __table_args__ = {
#         'schema': 'budget',  # Вьюхи обычно располагаются в другой схеме, например, 'budget'
#         'viewonly': True,
#         'comment': 'Вью для таблицы доходов, объединяющая информацию о пользователях и доходах'
#     }
#
#     __table__ = Table(
#         'income_view', Base.metadata,
#         Column('id', Integer, primary_key=True, comment="id дохода"),
#         Column('amount', Double, comment="Сумма дохода"),
#         Column('description', Text, comment="Описание дохода"),
#         Column('user_id', Integer, comment="id пользователя"),
#         Column('user_name', String(100), comment="Имя пользователя"),
#         Column('created_at', DateTime, comment="Дата и время создания дохода"),
#         schema='budget'
#     )
#
#     # Запрос для определения данных вьюхи
#     query = (
#         select(
#             Income.id,
#             Income.amount,
#             Income.description,
#             Income.user_id,
#             User.name.label('user_name'),
#             Income.created_at
#         )
#         .join(User, Income.user_id == User.id, isouter=True)  # Левое соединение для пользователей без доходов
#     )
