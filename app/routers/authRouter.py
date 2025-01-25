from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse, Response

from app.db.models.usersModel import MUser
from app.schemas.authSchemas import SUserRegister, SUserAuth
from app.service.authService import registerNewUsers, authenticate_user
from app.service.securityService import get_current_user
from app.utils.authUtils import create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    "/register",
    summary="Регистрация нового пользователя"
)
async def register_user(user_data: SUserRegister) -> JSONResponse:
    if user_data.role_name == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Невозможно зарегистрировать пользователя с ролью админ')
    try:
        new_user = await registerNewUsers(user_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": f"Пользователь с id {new_user.id} успешно создан"}
    )


@router.post(
    "/login",
    summary="Авторизация пользователя"
)
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный username или password')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        'status_code': status.HTTP_200_OK,
        'access_token': access_token
    }


@router.post(
    "/logout",
    summary="Выход из системы"
)
async def logout_user(response: Response, user_data: MUser = Depends(get_current_user)):
    response.delete_cookie(key="users_access_token")
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'{user_data.username} успешно вышел из системы')
