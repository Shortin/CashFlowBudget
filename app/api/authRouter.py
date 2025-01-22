from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.schemas.authSchemas import SUserRegister
from app.service.authService import registerNewUsers

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: SUserRegister) -> JSONResponse:
    new_user = await registerNewUsers(user_data)
    return JSONResponse(
        status_code=201,
        content={"message": f"Пользователь с id {new_user.id} успешно создан"}
    )
