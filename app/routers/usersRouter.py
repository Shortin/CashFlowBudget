from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.db.models.usersModel import MUser, RoleName
from app.schemas.usersSchemas import SUserUpdate, SUserPublic
from app.service.securityService import get_current_user, role_required
from app.service.usersService import get_user_by_id, patch_user, delete_user, get_user_by_username, get_users, \
    get_role_by_name
from app.utils.routerUtil import get_user_id

router = APIRouter(prefix='/user', tags=['User'])


@router.get(
    "/get_user_by_id",
    summary="Obtaining a user by ID or to himself",
    response_model=SUserPublic
)
async def get_user_by_id_endpoint(
        user_id: Optional[int] = Query(default=None),
        current_user: MUser = Depends(get_current_user)
):
    """
    Получить данные пользователя по ID. Если ID не указан, возвращается информация о текущем пользователе.
    """
    target_user_id = await get_user_id(user_id=user_id, user=current_user)

    user = await get_user_by_id(target_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {target_user_id} was not found."
        )

    # Преобразование в публичную модель для ответа
    return SUserPublic(
        id=user.id,
        name=user.name,
        birthday=user.birthday,
        username=user.username,
        role_name=user.role.name if user.role else None
    )


@router.get(
    "/get_user_by_username",
    summary="Obtaining a user named user",
    response_model=SUserPublic
)
async def get_user_by_username_endpoint(
        username: Optional[str] = Query(default=None),
        current_user: MUser = Depends(get_current_user)
):
    """
    Получить данные пользователя по имени пользователя. Доступно только для администраторов или самого пользователя.
    """
    # Если текущий пользователь запрашивает свои данные
    if (username == current_user.username
            or current_user.role.name == RoleName.ADMIN):
        user = await get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"A user named {username} was not found."
            )

        # Возвращаем публичное представление пользователя
        return SUserPublic(
            id=user.id,
            name=user.name,
            birthday=user.birthday,
            username=user.username,
            role_name=user.role.name if user.role else None
        )

    # Если текущий пользователь не администратор и пытается получить данные другого пользователя
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You cannot get the data of another user, if you are not an administrator."
    )


@router.patch(
    "/update",
    summary="User data update",
    response_model=SUserPublic
)
async def update_user_endpoint(
        user_update: SUserUpdate,
        user_id: Optional[int] = Query(default=None, description="ID user"),
        current_user: MUser = Depends(get_current_user)
):
    """
    Обновить данные пользователя. Только администратор может менять роль, и только сам пользователь может менять имя.
    """
    # Получаем ID пользователя для обновления
    user_update_id = await get_user_id(user_id=user_id, user=current_user)

    # Проверка прав на изменение роли
    if user_update.role_name and current_user.role != RoleName.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="The role of the user can only be changed by the administrator!"
        )

    # Проверка прав на изменение имени пользователя
    if user_update.username and user_update_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="The user name can only be changed by the user himself!"
        )

    # Получаем данные пользователя из базы
    user_to_update = await get_user_by_id(user_id=user_update_id)

    # Обновляем только изменённые поля
    fields_to_update = {
        "name": user_update.name,
        "birthday": user_update.birthday,
        "username": user_update.username,
        "role": await get_role_by_name(user_update.role_name) if user_update.role_name else None,
    }
    for field, value in fields_to_update.items():
        if value is not None:
            setattr(user_to_update, field, value)

    # Возвращаем успешный ответ
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User data successfully updated",
                 "user": jsonable_encoder(await patch_user(user_to_update))}
    )


@router.delete(
    "/delete_user",
    summary="Удаление пользователя по ID"
)
async def delete_user_endpoint(
        user_id: Optional[int] = Query(default=None, description="User ID"),
        current_user: MUser = Depends(get_current_user)
):
    """
    Удалить пользователя по ID.
    """
    # Получаем ID пользователя для удаления
    user_id_to_delete = await get_user_id(user_id=user_id, user=current_user)

    # Получаем пользователя по ID
    user_to_delete = await get_user_by_id(user_id=user_id_to_delete)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id_to_delete} was not found."
        )

    # Удаляем пользователя
    if not await delete_user(user_to_delete):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"User with ID {user_id_to_delete} was successfully removed."}
    )


@router.get(
    "/get_all_users",
    summary="Get a list of all users (only for administrators)",
    response_model=List[SUserPublic]
)
async def get_all_users_endpoint(
        admin_user: MUser = role_required(["admin"])  # noqa
):
    """
    Получить список всех пользователей. Этот эндпоинт доступен только администраторам.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"users": jsonable_encoder(await get_users())}
    )
