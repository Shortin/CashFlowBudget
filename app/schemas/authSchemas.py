from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.db.models.usersModel import User, Family, Role
from app.schemas.usersSchemas import FamilySchema


class SUserRegister(BaseModel):
    name: str = Field(..., min_length=5, max_length=25, description="Имя пользователя (от 5 до 50 знаков)",
                      examples=["Иванов Иван"])
    birthday: date = Field(..., ge=date(1960, 1, 1), description="Дата рождения пользователя", examples=['2000-01-01'])
    family: Optional[FamilySchema] = Field(None, description="Семья пользователя", examples=['{\n\t"id":1,\n\t"name":"name"\n}'])
    role_name: Role.RoleName = Field(..., description="Название роли пользователя", examples=["user"])
    username: str = Field(..., min_length=5, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
    password: str = Field(..., min_length=5, max_length=50, description="Пароль (от 5 до 50 знаков)")

    @classmethod
    @field_validator("birthday")
    def validate_phone_number(cls, value: date) -> date:
        if value > datetime.now().date():
            raise ValueError('Дата рождения не может быть больше сегодняшней')
        return value
