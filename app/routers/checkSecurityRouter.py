from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.db.models.usersModel import MUser
from app.service.securityService import get_current_user

router = APIRouter(prefix='/check', tags=['Check'])


@router.get(
    "/checkAuth",
    summary="Authorization check",
    description="This endpoint checks whether the current user is authorized."
)
async def get_check_auth_endpoint(
        user_data: MUser = Depends(get_current_user)
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f'You are authorized under the role: {user_data.role.name if user_data.role else None}'
    )


@router.get(
    "/ping",
    summary="Check connection",
    description="Check connection"
)
async def get_ping_endpoint():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Connection successful!'
    )
