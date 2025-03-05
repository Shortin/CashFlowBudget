from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.usersSchemas import SUserPublic


class STransactionPublic(BaseModel):
    id: int = Field(..., description="ID транзакции")
    amount: float = Field(..., description="Сумма транзакции", examples=[100.50])
    description: Optional[str] = Field(None, description="Описание транзакции", examples=["Оплата за подписку"])
    is_income: bool = Field(..., description="Флаг для типа транзакции: True - доход, False - расход", examples=[True])
    created_at: datetime = Field(..., description="Дата и время создания записи транзакции", examples=["2024-03-05T12:00:00Z"])
    user: SUserPublic = Field(..., description="Пользователь, который совершил транзакцию")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

class STransactionCreate(BaseModel):
    amount: float = Field(..., description="Сумма транзакции", examples=[100.50])
    description: Optional[str] = Field(None, description="Описание транзакции", examples=["Оплата за подписку"])
    is_income: bool = Field(..., description="Флаг дохода/расхода", examples=[False])

    class Config:
        from_attributes = True