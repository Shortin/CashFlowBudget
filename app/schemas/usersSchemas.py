from datetime import date
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from app.db.models.usersModel import MRole, RoleName


class SUserPublic(BaseModel):
    id: int
    name: Optional[str] = Field(None, examples=['New Name'])
    birthday: Optional[date] = Field(None, examples=['2012-12-21'])
    username: str = Field(..., min_length=4, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
    role_name: RoleName = Field(..., description="Название роли пользователя", examples=["user"])

    @field_validator('username', mode='before')
    def username_length(cls, value: str):
        if len(value) < 4 or len(value) > 25:
            raise HTTPException(status_code=400, detail='Username must be between 4 and 25 characters.')
        return value

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
        }


class SUserUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=['New Name'])
    birthday: Optional[date] = Field(None, examples=['2012-12-21'])
    username: Optional[str] = Field(None, min_length=4, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
    role_name: Optional[str] = Field(None, description="Название роли пользователя", examples=["user"])

    @field_validator('username', mode='before')
    def username_length(cls, value: str):
        if len(value) < 4 or len(value) > 25:
            raise HTTPException(status_code=400, detail='Username must be between 4 and 25 characters.')
        return value

    @field_validator('role_name', mode='before')
    def role_name_check(cls, value: str):
        if value not in ['user', 'admin']:
            raise HTTPException(status_code=400, detail='Such a role does not dry!')
        return value

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
        }


class SUserUpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=4, title="Текущий пароль", description="Текущий пароль пользователя.")
    new_password: str = Field(..., min_length=4, title="Новый пароль", description="Новый пароль пользователя.")

    class Config:
        str_strip_whitespace = True


class SUserUpdateRole(BaseModel):
    role_name: RoleName = Field(..., description="Название роли пользователя", examples=["user"])
    username: str = Field(..., min_length=5, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
