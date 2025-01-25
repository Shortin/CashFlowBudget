from datetime import date, datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from app.db.models.usersModel import MRole


class SUserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=25, description="Имя пользователя (от 5 до 50 знаков)",
                      examples=["Иванов Иван"])
    birthday: date = Field(..., ge=date(1960, 1, 1), description="Дата рождения пользователя", examples=['2000-01-01'])
    role_name: MRole.RoleName = Field(..., description="Название роли пользователя", examples=["user"])
    username: str = Field(..., min_length=4, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
    password: str = Field(..., min_length=5, max_length=50, description="Пароль (от 5 до 50 знаков)")

    @field_validator('username', mode='before')
    def username_length(cls, value: str):
        if len(value) < 4 or len(value) > 25:
            raise HTTPException(status_code=400, detail='Username must be between 4 and 25 characters.')
        return value

    @field_validator('password', mode='before')
    def password_length(cls, value):
        if len(value) < 5 or len(value) > 50:
            raise HTTPException(status_code=400, detail='Password must be between 5 and 50 characters.')
        return value

    @field_validator("birthday", mode='before')
    def validate_birthday(cls, value: date) -> date:
        birthday_date = datetime.strptime(value, "%Y-%m-%d").date()

        if birthday_date > datetime.now().date():
            raise HTTPException(status_code=400, detail='The date of birth cannot be more of today\'s')
        return value


class SUserAuth(BaseModel):
    username: str = Field(..., min_length=5, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
    password: str = Field(..., min_length=5, max_length=50, description="Пароль (от 5 до 50 знаков)")
