from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Схема для отображения расхода
class ExpenseBase(BaseModel):
    amount: float  # Сумма расхода
    description: Optional[str] = None  # Описание расхода
    created_at: datetime  # Дата и время создания расхода
    user_id: int  # Идентификатор пользователя, который сделал расход

    class Config:
        from_attributes = True


# Схема для создания расхода (без id, для POST-запросов)
class ExpenseCreate(ExpenseBase):
    amount: float  # Сумма расхода
    description: Optional[str] = None  # Описание расхода
    user_id: int  # Идентификатор пользователя, который сделал расход

    class Config:
        from_attributes = True


# Схема для обновления данных расхода
class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None  # Сумма расхода
    description: Optional[str] = None  # Описание расхода

    class Config:
        from_attributes = True


# Схема для вывода подробной информации о расходе
class ExpenseDetail(ExpenseBase):
    user_id: int  # Имя пользователя, который сделал расход (для детализации)

    class Config:
        from_attributes = True


# Схема для отображения дохода
class IncomeBase(BaseModel):
    amount: float
    description: Optional[str] = None
    created_at: datetime
    user_id: int  # Добавляем user_name или другие необходимые поля

    class Config:
        from_attributes = True

class IncomeCreate(BaseModel):
    amount: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Схема для обновления данных дохода
class IncomeUpdate(BaseModel):
    amount: Optional[float] = None  # Сумма дохода
    description: Optional[str] = None  # Описание дохода

    class Config:
        from_attributes = True


# Схема для вывода подробной информации о доходе
class IncomeDetail(IncomeBase):
    user_id: int  # Имя пользователя, который сделал доход (для детализации)

    class Config:
        from_attributes = True
