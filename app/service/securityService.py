from datetime import datetime, timezone
from typing import List

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from app.config import get_auth_data
from app.db.models.usersModel import MUser
from app.service.usersService import get_user_by_id
from app.utils.authUtils import get_token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


def role_required(allowed_roles: List[str]):
    async def decorator(user: MUser = Depends(get_current_user)):
        if "admin" in user.role.name and "admin" not in allowed_roles:
            allowed_roles.append("admin")

        if user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен"
            )
        return user

    return Depends(decorator)
