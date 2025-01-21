from typing import Optional

from sqlalchemy.future import select

from app.db.models.usersModel import Role
from app.db.session import get_sessions


async def get_role_id_by_name(role_name: str) -> Optional[int]:
    async with get_sessions() as session:
        # Строим запрос на поиск роли по имени
        result = await session.execute(select(Role.id).filter_by(name=role_name))
        return result.scalar_one_or_none() # Если роле не существует, вернется None