from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Double
from sqlalchemy.orm import relationship

from app.db.session import Base  # Импортируем базовый класс из db


# Таблица расходов, представляет расходы пользователей.
class MExpense(Base):
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
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        comment="Дата и время создания записи расхода")

    # Связь с таблицей пользователей (User)
    user = relationship("MUser", back_populates="expenses", lazy="joined")


# Таблица доходов, представляет доходы пользователей.
class MIncome(Base):
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
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        comment="Дата и время создания записи дохода")

    # Связь с таблицей пользователей (User)
    user = relationship("MUser", back_populates="incomes", lazy="joined")
