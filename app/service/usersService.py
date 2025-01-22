from typing import Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.usersModel import MRole, MFamily, MUser
from app.db.session import get_sessions
from app.schemas.usersSchemas import SFamilySchema


class QueryBuilder:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session  # Сессия передается в конструктор
        self.filters = []
        self.or_filters = []  # Для OR фильтров

    def filter_by(self, **kwargs):
        """Добавляет фильтры к запросу, игнорируя те, что равны None"""
        for key, value in kwargs.items():
            if value is not None:
                if key == "id" or key == "name":  # Пример логики OR для этих полей
                    self.or_filters.append(getattr(self.model, key) == value)
                else:  # Все остальные фильтры применяем через AND
                    self.filters.append(getattr(self.model, key) == value)
        return self

    async def build(self):
        """Строит запрос с добавленными фильтрами и выполняет его с помощью сессии"""
        query = select(self.model)

        if self.filters:
            query = query.filter(and_(*self.filters))  # AND для других фильтров

        # Выполняем запрос с использованием сессии и возвращаем все результаты
        result = await self.session.execute(query)
        return result.scalars().all()  # Используем .scalars() для получения объектов

"""
    User
"""

async def get_user_by_username(username: str) -> Optional[MUser]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MUser, session)
        query_builder.filter_by(username=username)  # Здесь используем username
        result = await query_builder.build()
        return result[0] if result else None

async def get_user_by_id(user_id: int) -> Optional[MUser]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MUser, session)
        query_builder.filter_by(id=user_id)  # Здесь используем username
        result = await query_builder.build()
        return result[0] if result else None



"""
    Role
"""

async def get_role(role: MRole) -> Optional[MRole]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MRole, session)
        query_builder.filter_by(id=role.id, name=role.name)  # Здесь используем объекты role
        result = await query_builder.build()
        return result[0] if result else None



"""
    Family
"""
async def get_family(family: SFamilySchema) -> Optional[MFamily]:
    async with get_sessions() as session:
        # Создаем экземпляр QueryBuilder, передавая модель и сессию
        query_builder = QueryBuilder(MFamily, session)

        # Добавляем фильтры по id и name
        query_builder.filter_by(id=family.id, name=family.name)  # Используем объекты family

        # Строим и выполняем запрос
        result = await query_builder.build()

        # Возвращаем первый результат (если есть)
        return result[0] if result else None
