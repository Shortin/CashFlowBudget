from typing import Optional

from fastapi import HTTPException

from app.db.models.usersModel import MUser, RoleName


async def get_user_id(
        user_id: Optional[int],
        user: MUser
) -> int:
    """
    Получает ID пользователя для выполнения операций, проверяя права доступа.

    Если `user_id` не передан, возвращается ID текущего пользователя.
    Если `user_id` передан, проверяется, имеет ли текущий пользователь права для работы с указанным ID:
        - Если текущий пользователь администратор (роль ADMIN), то операция разрешена.
        - Если текущий пользователь пытается работать с собственным ID, то операция разрешена.
        - В противном случае выбрасывается исключение.

    Args:
        user_id (Optional[int]): ID пользователя, переданный для проверки. Если None, используется ID текущего пользователя.
        user (MUser): Объект текущего пользователя, включающий его ID и роль.

    Returns:
        int: Идентификатор пользователя, который будет использоваться для выполнения операций.

    Raises:
        HTTPException: Если пользователь пытается работать с ID другого пользователя и не является администратором.
        HTTPException: status_code=403, detail="You cannot access another user's data unless you are an admin"
    """
    if user_id is None:
        return user.id

    if user.role.name == RoleName.ADMIN or user_id == user.id:
        return user_id

    raise HTTPException(
        status_code=403,
        detail="You cannot access another user's data unless you are an admin"
    )