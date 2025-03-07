from datetime import datetime, timezone
from typing import List

import jwt
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.config import get_auth_data
from app.db.models.usersModel import MUser
from app.service.usersService import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_token_from_request(request: Request) -> str:
    token_from_header = request.headers.get("Authorization")
    if token_from_header:
        token_from_header = token_from_header.split(" ")[1]

    token_from_cookie = request.cookies.get("users_access_token")

    if token_from_header:
        return token_from_header
    elif token_from_cookie:
        return token_from_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found"
        )


async def get_current_user(request: Request, token: str = Depends(get_token_from_request)) -> MUser:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid!")

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")

    user = await get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def role_required(allowed_roles: List[str]):
    async def decorator(user: MUser = Depends(get_current_user)):
        if "admin" in user.role.name and "admin" not in allowed_roles:
            allowed_roles.append("admin")

        if user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )
        return user

    return Depends(decorator)
