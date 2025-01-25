from typing import Optional, List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn.server import logger

from app.db.models.usersModel import MRole, MUser
from app.db.session import get_sessions
from app.schemas.usersSchemas import SUserPublic


class QueryBuilder:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session
        self.filters = []
        self.or_filters = []

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
            query = query.filter(and_(*self.filters))

        result = await self.session.execute(query)
        return result.scalars().all()


"""
    User
"""


async def get_users() -> List[SUserPublic]:
    """
    Получить список всех пользователей.
    """
    async with get_sessions() as session:
        query_builder = QueryBuilder(MUser, session)
        result = await query_builder.build()

        users = [
            SUserPublic(
                id=user.id,
                name=user.name,
                birthday=user.birthday,
                username=user.username,
                role_name=user.role.name if user.role else "No Role"
            )
            for user in result
        ]

        return users


async def get_user_by_username(username: str) -> Optional[MUser]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MUser, session)
        query_builder.filter_by(username=username)
        result = await query_builder.build()
        return result[0] if result else None


async def get_user_by_id(user_id: int) -> Optional[MUser]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MUser, session)
        query_builder.filter_by(id=user_id)
        result = await query_builder.build()
        return result[0] if result else None


async def patch_user(user_data: MUser) -> SUserPublic:
    async with get_sessions() as session:
        session.add(user_data)
        await session.commit()
        await session.refresh(user_data)
        role_name = user_data.role.name if user_data.role else None
        user_public = SUserPublic(
            id=user_data.id,
            name=user_data.name,
            birthday=user_data.birthday,
            role_name=role_name
        )

        return user_public


async def delete_user(user_data: MUser) -> bool:
    async with get_sessions() as session:
        try:
            await session.delete(user_data)
            await session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False


"""
    Role
"""


async def get_role(role: MRole) -> Optional[MRole]:
    async with get_sessions() as session:
        query_builder = QueryBuilder(MRole, session)
        query_builder.filter_by(id=role.id, name=role.name)
        result = await query_builder.build()
        return result[0] if result else None
