from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.db.models.usersModel import MRole


class SFamilySchema(BaseModel):
    id: Optional[int] = Field(None, examples=['1'])
    name: Optional[str] = Field(None, examples=['FamilyName'])


class SUserPublic(BaseModel):
    id: int  # Идентификатор пользователя
    name: Optional[str] = Field(None, examples=['New Name'])
    birthday: Optional[date] = Field(None, examples=['2012-12-21'])
    family_name: Optional[SFamilySchema] = Field(None, description="Семья пользователя",
                                                 examples=['{\n\t"id":1,\n\t"name":"name"\n}'])
    role_name: str  # Роль пользователя

    class Config:
        from_attributes = True  # Для работы с SQLAlchemy моделями
        json_encoders = {
            date: lambda v: v.isoformat(),  # Автоматическое преобразование даты в строку
        }


class SUserUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=['New Name'])
    birthday: Optional[date] = Field(None, examples=['2012-12-21'])
    family: Optional[SFamilySchema] = Field(None, description="Семья пользователя",
                                            examples=['{\n\t"id":1,\n\t"name":"name"\n}'])


class SUserUpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=4, title="Текущий пароль", description="Текущий пароль пользователя.")
    new_password: str = Field(..., min_length=4, title="Новый пароль", description="Новый пароль пользователя.")

    class Config:
        str_strip_whitespace = True  # Убираем пробелы по краям


class SUserUpdateRole(BaseModel):
    role_name: MRole.RoleName = Field(..., description="Название роли пользователя", examples=["user"])
    username: str = Field(..., min_length=5, max_length=25,
                          description="Уникальный username пользователя (от 5 до 50 знаков)", examples=["username"])
