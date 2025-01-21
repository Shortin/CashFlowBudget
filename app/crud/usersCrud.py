from app.db.models.usersModel import *
from app.schemas.usersSchemas import *
from app.utils.crud_utils import create_entity, get_entity, get_entities, update_entity, delete_entity


# CRUD для User
async def create_user_db(user: UserCreate):
    """
    Создает нового пользователя (User) в базе данных.

    - **db**: Сессия базы данных.
    - **user**: Данные пользователя, которые необходимо сохранить.

    Возвращает созданного пользователя.
    """

    return await create_entity(
        User,
        name=user.name,
        birthday=user.birthday,
        username=user.username,
        password_hash=user.password_hash,
        family_id=user.family_id,
        role_id=user.role_id,
    )


async def get_user_db(user_id: int):
    """
    Получает пользователя по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **user_id**: Уникальный идентификатор пользователя.

    Возвращает объект пользователя или None, если пользователь не найден.
    """
    user = await get_entity(User, user_id)
    if user:
        return UserBase(
            name=user.name,
            birthday=user.birthday,
            username=user.username,
            family_id=user.family_id,
            role_id=user.role_id
        )
    return None


async def get_users_db(skip: int = 0, limit: int = 100):
    """
    Получает список пользователей с возможностью пропуска и ограничения.

    - **db**: Сессия базы данных.
    - **skip**: Количество пользователей для пропуска (по умолчанию 0).
    - **limit**: Количество пользователей для возврата (по умолчанию 100).

    Возвращает список пользователей.
    """
    # Не забываем добавить await
    users = await get_entities(User, skip, limit)
    return [
        UserBase(
            name=user.name,
            birthday=user.birthday,
            username=user.username,
            family_id=user.family_id,
            role_id=user.role_id
        )
        for user in users
    ]



async def update_user_db(user_id: int, user: UserUpdate):
    """
    Обновляет данные пользователя по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **user_id**: Уникальный идентификатор пользователя.
    - **user**: Данные для обновления пользователя.

    Возвращает обновленного пользователя или None, если пользователь не найден.
    """
    return await update_entity(User, user_id, user.model_dump(exclude_unset=True))


async def delete_user_db(user_id: int):
    """
    Удаляет пользователя по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **user_id**: Уникальный идентификатор пользователя.

    Возвращает удаленного пользователя или None, если пользователь не найден.
    """
    return await delete_entity(User, user_id)


# CRUD для Family
async def create_family_db(family: FamilyBase):
    """
    Создает новую семью (Family) в базе данных.

    - **db**: Сессия базы данных.
    - **family**: Данные семьи, которые необходимо сохранить.

    Возвращает созданную семью.
    """
    return await create_entity(
        Family,
        family_name=family.family_name,
        description=family.description,
    )


async def get_family_db(family_id: int):
    """
    Получает семью по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **family_id**: Уникальный идентификатор семьи.

    Возвращает объект семьи или None, если семья не найдена.
    """
    family = await get_entity(Family, family_id)
    if family:
        return FamilyBase(
            family_name=family.family_name,
            description=family.description,
        )
    return None


async def get_families_db(skip: int = 0, limit: int = 100):
    """
    Получает список семей с возможностью пропуска и ограничения.

    - **db**: Сессия базы данных.
    - **skip**: Количество семей для пропуска (по умолчанию 0).
    - **limit**: Количество семей для возврата (по умолчанию 100).

    Возвращает список семей.
    """
    return await get_entities(Family, skip, limit)


async def update_family_db(family_id: int, family: FamilyBase):
    """
    Обновляет данные семьи по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **family_id**: Уникальный идентификатор семьи.
    - **family**: Данные для обновления семьи.

    Возвращает обновленную семью или None, если семья не найдена.
    """
    return await update_entity(Family, family_id, family.model_dump(exclude_unset=True))


async def delete_family_db(family_id: int):
    """
    Удаляет семью по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **family_id**: Уникальный идентификатор семьи.

    Возвращает удаленную семью или None, если семья не найдена.
    """
    return await delete_entity(Family, family_id)


# CRUD для Role
async def create_role_db(role: RoleBase):
    """
    Создает новую роль (Role) в базе данных.

    - **db**: Сессия базы данных.
    - **role**: Данные роли, которые необходимо сохранить.

    Возвращает созданную роль.
    """
    return await create_entity(Role, name=role.name)


async def get_role_db(role_id: int):
    """
    Получает роль по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **role_id**: Уникальный идентификатор роли.

    Возвращает объект роли или None, если роль не найдена.
    """
    role = await get_entity(Role, role_id)
    if role:
        return RoleBase(
            name=role.name,
        )
    return None

async def get_roles_db(skip: int = 0, limit: int = 100):
    """
    Получает список ролей с возможностью пропуска и ограничения.

    - **db**: Сессия базы данных.
    - **skip**: Количество ролей для пропуска (по умолчанию 0).
    - **limit**: Количество ролей для возврата (по умолчанию 100).

    Возвращает список ролей.
    """
    roles = await get_entities(Role, skip, limit)
    return [
        RoleBase(name=role.name)
        for role in roles
    ]


async def update_role_db(role_id: int, role: RoleBase):
    """
    Обновляет данные роли по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **role_id**: Уникальный идентификатор роли.
    - **role**: Данные для обновления роли.

    Возвращает обновленную роль или None, если роль не найдена.
    """
    return await update_entity(Role, role_id, role.model_dump(exclude_unset=True))


async def delete_role_db(role_id: int):
    """
    Удаляет роль по уникальному идентификатору.

    - **db**: Сессия базы данных.
    - **role_id**: Уникальный идентификатор роли.

    Возвращает удаленную роль или None, если роль не найдена.
    """
    return await delete_entity(Role, role_id)
