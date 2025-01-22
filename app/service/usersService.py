from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn.server import logger

from app.db.models.usersModel import MRole, MFamily, MUser
from app.db.session import get_sessions
from app.schemas.usersSchemas import SFamilySchema, SUserPublic


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


async def patch_user(user_data: MUser) -> SUserPublic:
    async with get_sessions() as session:
        # Сохраняем изменения в базе данных
        session.add(user_data)
        await session.commit()
        await session.refresh(user_data)
        role_name = user_data.role.name if user_data.role else None
        user_public = SUserPublic(
            id=user_data.id,
            name=user_data.name,
            birthday=user_data.birthday,
            family=user_data.family,
            role_name=role_name
        )

        return user_public


async def delete_user(user_data: MUser) -> bool:
    async with get_sessions() as session:
        try:
            # Удаляем пользователя из базы данных
            await session.delete(user_data)
            await session.commit()
            return True
        except Exception as e:
            # Если произошла ошибка при удалении, возвращаем False
            logger.error(e)
            return False


"""
    Role
"""


async def get_role(role: MRole) -> Optional[MRole]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MRole, session)
        # Используем строгие условия для поиска по id и name
        query_builder.filter_by(id=role.id, name=role.name)
        result = await query_builder.build()
        return result[0] if result else None


"""
    Family
"""


async def get_family(family: SFamilySchema) -> Optional[MFamily]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MRole, session)
        # Используем строгие условия для поиска по id и name
        query_builder.filter_by(id=family.id, name=family.name)
        result = await query_builder.build()
        return result[0] if result else None
