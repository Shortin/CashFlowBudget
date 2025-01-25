from datetime import datetime
from http.client import HTTPException
from typing import Optional

from pydantic import BaseModel, model_validator


# Схема для отображения расхода
class TransactionBase(BaseModel):
    amount: float  # Сумма расхода
    description: Optional[str] = None  # Описание расхода
    created_at: datetime  # Дата и время создания расхода
    user_id: int  # Идентификатор пользователя, который сделал расход

    # Валидация на уровне всей модели
    @model_validator(mode='before')
    def validate_fields(self, values):
        amount = values.get('amount')
        created_at = values.get('created_at')

        # Валидация, чтобы сумма расходов была больше нуля
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")

        # Валидация, чтобы дата не была в будущем
        if created_at > datetime.now():
            raise HTTPException(status_code=400, detail="Created at cannot be in the future")

        return values

    class Config:
        from_attributes = True


# Схема для создания расхода (без id, для POST-запросов)
class TransactionCreate(TransactionBase):
    amount: float  # Сумма расхода
    description: Optional[str] = None  # Описание расхода
    user_id: int  # Идентификатор пользователя, который сделал расход

    class Config:
        from_attributes = True


# Схема для обновления данных расхода
class TransactionUpdateBase(BaseModel):
    amount: Optional[float] = None  # Сумма расхода
    description: Optional[str] = None  # Описание расхода

    class Config:
        from_attributes = True


# # Схема для вывода подробной информации о расходе
class TransactionDetail(TransactionBase):
    user_id: int  # Имя пользователя, который сделал расход (для детализации)

    class Config:
        from_attributes = True


class IncomeCreate(BaseModel):
    amount: float
    description: Optional[str] = None

    class Config:
        from_attributes = True
