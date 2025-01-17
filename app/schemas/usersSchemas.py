from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


# Схема для отображения роли пользователя
class RoleBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


# Схема для отображения семьи
class FamilyBase(BaseModel):
    family_name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Схема для отображения пользователя
class UserBase(BaseModel):
    name: str
    birthday: Optional[datetime] = None
    username: str
    password_hash: str
    created_at: datetime
    family_id: Optional[int] = None
    role_id: Optional[int] = None

    class Config:
        from_attributes = True


# Схема для создания пользователя (без id, для POST-запросов)
class UserCreate(UserBase):
    password_hash: str  # Для создания мы передаем хэш пароля


# Схема для обновления данных пользователя
class UserUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[datetime] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    family_id: Optional[int] = None
    role_id: Optional[int] = None

    class Config:
        from_attributes = True


# Схема для вывода подробной информации о пользователе с включением связанных данных
class UserDetail(UserBase):
    family: Optional[FamilyBase] = None
    role: Optional[RoleBase] = None

    class Config:
        from_attributes = True


# Схема для вывода информации о семье
class FamilyDetail(FamilyBase):
    members: List[UserBase] = []

    class Config:
        from_attributes = True


# Схема для вывода информации о роли
class RoleDetail(RoleBase):
    users: List[UserBase] = []

    class Config:
        from_attributes = True
