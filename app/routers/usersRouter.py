from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from uvicorn.server import logger

from app.db.models.usersModel import MUser, MRole
from app.schemas.usersSchemas import SUserUpdate, SUserUpdatePassword, SUserUpdateRole, SUserPublic
from app.service.securityService import get_current_user, role_required
from app.service.usersService import get_user_by_id, patch_user, delete_user, get_user_by_username, get_role, \
    get_family, get_users
from app.utils.authUtils import verify_password, get_password_hash

router = APIRouter(prefix='/user', tags=['User'])


# Эндпоинт для обновления данных пользователя
@router.patch(
    "/update",
    summary="Обновить данные пользователя",
    description="Этот эндпоинт позволяет администратору или пользователю, которому принадлежит аккаунт, изменить свои данные."
)
async def update_user_data(
        user_data: SUserUpdate,
        current_user: MUser = Depends(get_current_user)
):
    user_to_update = await get_user_by_id(user_id=current_user.id)

    # Обновляем данные пользователя
    if user_data.name:
        user_to_update.name = user_data.name
    if user_data.birthday:
        user_to_update.birthday = user_data.birthday

    if user_data.family:
        family = await get_family(user_data.family)
        if family.id is not None:
            user_to_update.family_id = family.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такая семья не найдена"
            )

    updated_user = await patch_user(user_to_update)
    user_data_dict = updated_user.model_dump()
    user_data_dict['birthday'] = user_data_dict['birthday'].isoformat()  # Преобразуем дату в строку

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User data updated successfully", "user": user_data_dict}
    )


@router.patch(
    "/update_password",
    summary="Обновление пароля пользователя",
    description="Эндпоинт позволяет пользователю обновить свой пароль, если он предоставит правильный текущий пароль."
)
async def user_password_update(
        user_data: SUserUpdatePassword,
        current_user: MUser = Depends(get_current_user)
):
    if not verify_password(user_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный текущий пароль"
        )

    # Обновляем пароль
    current_user.password_hash = get_password_hash(user_data.new_password)
    await patch_user(current_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Пароль успешно обновлен."}
    )


@router.patch(
    "/update_userRole",
    summary="Обновление роли пользователя",
    description="Эндпоинт позволяет администратору обновить роль пользователя."
)
async def update_user_role(
        update_data: SUserUpdateRole,
        user_admin: MUser = role_required(["admin"])
):
    # Получаем пользователя по ID
    user_to_update = await get_user_by_username(update_data.username)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    role = await get_role(MRole(name=update_data.role_name))
    if role is None:
        raise HTTPException(status_code=404, detail=f"Role named {update_data.role_name} not found")
    user_to_update.role_id = role.id

    await patch_user(user_to_update)
    logger.info(f"Администратор {user_admin.name} изменяет роль пользователя с {user_to_update.name}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Теперь роль пользователя {user_to_update.name}: {role.name}"}
    )


@router.delete(
    "/self_delete",
    summary="Удалить себя",
    description="Этот эндпоинт позволяет пользователю удалить свой аккаунт и удалить токен из кук."
)
async def delete_user_self(response: Response, user_data: MUser = Depends(get_current_user)):
    if await delete_user(user_data):
        # Удаляем токен из кук
        response.delete_cookie(key="users_access_token")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Ваш аккаунт был успешно удален и вы вышли из системы."}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Не удалось удалить аккаунт."}
        )


@router.delete(
    "/delete_user/{user_id}",
    summary="Удалить пользователя по ID",
    description="Этот эндпоинт позволяет администратору или авторизованному пользователю удалять учетные записи других пользователей по их ID."
)
async def delete_user_by_id(user_id: int, user_admin: MUser = role_required(["admin"])):
    # Удаляем пользователя
    user_to_delete = await get_user_by_id(user_id)  # Получаем пользователя из базы по ID
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с указанным ID не найден."
        )

    if await delete_user(user_to_delete):  # Функция удаления пользователя
        logger.info(f"Администратор {user_admin.name} удаляет пользователя с ID {user_id}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Пользователь с ID {user_id} успешно удален."}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось удалить пользователя."
        )


@router.get(
    "/get_all_users",
    summary="Получить список всех пользователей (только для админа)",
    description="Этот эндпоинт возвращает список всех пользователей. Доступен только для администраторов.",
    response_model=List[SUserPublic]
)
async def get_all_users( user_admin: MUser = role_required(["admin"])):
    users = await get_users()  # Получаем список пользователей из базы данных
    # Преобразуем каждую модель MUser в Pydantic-схему SUserPublic
    serialized_users = [SUserPublic(**user.__dict__).model_dump() for user in users]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"users": serialized_users}
    )


@router.get(
    "/get_me",
    summary="Получить данные о себе",
    description="Этот эндпоинт позволяет авторизованному пользователю получить свои данные.",
    response_model=SUserPublic  # Указываем схему для сериализации данных в ответе
)
async def get_me(current_user: MUser = Depends(get_current_user)):
    # Преобразуем текущего пользователя в схему SUserPublic
    user_public = SUserPublic(
        id=current_user.id,
        name=current_user.name,
        birthday=current_user.birthday,
        family=current_user.family,
        role_name=current_user.role.name if current_user.role else None
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_public.model_dump()  # Используем model_dump для возврата данных
    )


@router.get(
    "/get_user_by_id/{user_id}",
    summary="Получить пользователя по ID",
    description="Этот эндпоинт позволяет получить данные пользователя по его ID.",
    response_model=SUserPublic  # Указываем схему для сериализации данных в ответе
)
async def get_user_by_id_endpoint(user_id: int,  user_admin: MUser = role_required(["admin"])):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким ID не найден."
        )
    # Преобразуем пользователя в объект схемы SUserPublic
    user_public = SUserPublic(
        id=user.id,
        name=user.name,
        birthday=user.birthday,
        family=user.family,
        role_name=user.role.name if user.role else None
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_public.model_dump()  # Используем model_dump для возврата данных
    )


@router.get(
    "/get_user_by_username/{username}",
    summary="Получить пользователя по имени пользователя (username)",
    description="Этот эндпоинт позволяет администратору получить данные пользователя по его username.",
    response_model=SUserPublic  # Указываем схему для сериализации данных в ответе
)
async def get_user_by_username_endpoint(username: str,  user_admin: MUser = role_required(["admin"])):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким username не найден."
        )
    # Преобразуем пользователя в объект схемы SUserPublic
    user_public = SUserPublic(
        id=user.id,
        name=user.name,
        birthday=user.birthday,
        family=user.family,
        role_name=user.role.name if user.role else None
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_public.model_dump()  # Используем model_dump для возврата данных
    )
