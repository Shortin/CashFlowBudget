from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Double, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base

class MTransaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = {
        'schema': 'data',
        'comment': 'Объединенная таблица доходов и расходов пользователей'
    }

    id = Column(Integer, primary_key=True, comment="id")
    amount = Column(Double, nullable=False, comment="Сумма транзакции")
    description = Column(Text, nullable=True, comment="Описание транзакции")
    is_income = Column(Boolean, nullable=False, comment="Флаг для типа транзакции: True - доход, False - расход")
    user_id = Column(Integer, ForeignKey('data.users.id'), nullable=False, comment="Ссылка на пользователя, который сделал транзакцию")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), comment="Дата и время создания записи транзакции")

    user = relationship("MUser", lazy="joined")

    def __repr__(self):
        return f"<MTransaction(id={self.id}, amount={self.amount}, description={self.description}, is_income={self.is_income}, user_id={self.user_id}, created_at={self.created_at})>"