from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.db.models.usersModel import MUser, MRole
from app.db.session import get_sessions
from app.schemas.authSchemas import SUserRegister
from app.service.usersService import get_role, get_family, get_user_by_username
from app.utils.authUtils import get_password_hash, verify_password


async def registerNewUsers(user_data: SUserRegister):
    new_user = MUser(
        name=user_data.name,
        birthday=user_data.birthday,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        created_at=datetime.now(tz=timezone.utc)
    )

    mRole = MRole()
    mRole.name = user_data.role_name
    role = await get_role(mRole)
    if role is None:
        raise ValueError(f"Роль с именем {user_data.role_name} не найдена")
    new_user.role_id = role.id

    if user_data.family is not None:
        family = await get_family(user_data.family)
        if family is None:
            if user_data.family.id is not None and user_data.family.name is not None:
                raise ValueError(f"Семья с таким id: {user_data.family.id} или с таким name: {user_data.family.name} не найдена.")
            elif user_data.family.id is not None:
                raise ValueError(f"Семья с таким id: {user_data.family.id} не найдена.")
            else:
                raise ValueError(f"Семья с таким name: {user_data.family.name} не найдена.")
        else:
            new_user.family_id = family.id

    async with get_sessions() as session:
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await session.rollback()
            raise e


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username=username)
    if not user or verify_password(plain_password=password, hashed_password=user.password_hash) is False:
        return None
    return user