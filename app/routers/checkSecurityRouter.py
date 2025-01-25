from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.db.models.usersModel import MUser
from app.service.securityService import role_required, get_current_user

router = APIRouter(prefix='/check', tags=['Check'])


@router.get(
    "/checkAuth",
    summary="Проверка авторизации",
    description="Этот эндпоинт проверяет, авторизован ли текущий пользователь."
)
async def get_me(user_data: MUser = Depends(get_current_user)):
    if user_data is not None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Вы авторизованы'
        )


@router.get(
    "/admin_only",
    summary="Доступ только для администраторов",
    description="Эндпоинт доступен только пользователям с ролью 'admin'."
)
async def admin_only_route(user: MUser = role_required(["admin"])):
    return {"message": "Только для администраторов"}


@router.get(
    "/user_only",
    summary="Доступ только для пользователей",
    description="Эндпоинт доступен только пользователям с ролью 'user'."
)
async def user_only_route(user: MUser = role_required(["user"])):
    return {"message": "Только для пользователей"}


@router.get(
    "/all_auth_users",
    summary="Доступ для всех авторизованных пользователей",
    description="Этот эндпоинт доступен всем пользователям, которые авторизовались в системе."
)
async def all_auth_users_route(user: MUser = Depends(get_current_user)):
    return {"message": "Для всех авторизованных пользователей"}


@router.get(
    "/all_users",
    summary="Доступ для всех пользователей",
    description="Эндпоинт доступен всем пользователям, включая неавторизованных."
)
async def all_users_route():
    return {"message": "Для всех пользователей"}
