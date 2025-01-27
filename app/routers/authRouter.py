from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from starlette.responses import JSONResponse, Response

from app.db.models.usersModel import MUser
from app.schemas.authSchemas import SUserRegister, SUserAuth
from app.schemas.usersSchemas import SUserUpdatePassword
from app.service.authService import registerNewUsers, authenticate_user
from app.service.securityService import get_current_user
from app.service.usersService import patch_user
from app.utils.authUtils import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    "/register",
    summary="Registration of a new user"
)
async def post_register_user_endpoint(
        response: Response,
        user_data: SUserRegister,
        is_authorization: Optional[bool] = Query(True,
                                                 description="If true, the user will be automatically logged in after registration")
):
    """
    Зарегистрируйте нового пользователя. Если is_authorization true, пользователь будет автоматически авторизован.
    """
    # Check if the user is trying to register with the 'admin' role
    if user_data.role_name == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='It is impossible to register a user with the role of admin'
        )

    try:
        # Attempt to register the new user
        new_user = await registerNewUsers(user_data)
    except Exception as e:
        # Handle errors during registration (e.g., if the username already exists)
        if "username" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken. Please choose a different one."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It was not possible to create a new user"
        )

    # If authorization is required, generate an access token and set it as a cookie
    if is_authorization:
        access_token = create_access_token({"sub": str(new_user.id)})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    # Return a success message with the newly created user's ID
    return {
        'status_code': status.HTTP_201_CREATED,
        'access_token': {"message": f"User with ID {new_user.id} successfully created"}
    }


@router.post(
    "/login",
    summary="User Login"
)
async def post_login_endpoint(
        response: Response,
        user_data: SUserAuth
):
    """
   Аутентификация пользователя и генерация токена доступа.
    """
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        'status_code': status.HTTP_200_OK,
        'access_token': access_token
    }


@router.patch(
    "/update_password",
    summary="User Password Update"
)
async def patch_update_password_endpoint(
        user_data: SUserUpdatePassword,
        current_user: MUser = Depends(get_current_user)
):
    """
    Данный метод обновляет пароль пользователя.
    """
    if not verify_password(user_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong current password"
        )

    # Update password and save changes
    current_user.password_hash = get_password_hash(user_data.new_password)
    await patch_user(current_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The password was successfully updated."}
    )


@router.post(
    "/logout",
    summary="User Logout"
)
async def post_logout_endpoint(
        response: Response,
        user_data: MUser = Depends(get_current_user)
):
    """
    Данный метод удаляет пользователя из системы и чистит куки.
    """
    response.delete_cookie(key="users_access_token")
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f'{user_data.username} successfully logged out'
    )
