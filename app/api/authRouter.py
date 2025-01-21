from fastapi import APIRouter

from app.schemas.authSchemas import SUserRegister

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: SUserRegister) -> dict:

    return {'message': 'Вы успешно зарегистрированы!'}
