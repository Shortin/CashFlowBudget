from fastapi import APIRouter

router = APIRouter(prefix='/finances', tags=['Finances'])


# @router.get(
#     "/transactions",
#     summary="Получить все транзакции",
#     description="Эндпоинт для получения всех транзакций из базы данных."
# )
# async def get_transactions(
#         user_admin: MUser = role_required(["admin"]) # noqa
# ):
#     transactions = await get_all_transactions()
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={"transactions": jsonable_encoder(transactions)}
#     )
#
# @router.get(
#     "/transactions/user/{user_id}",
#     summary="Получить транзакции пользователя",
#     description="Эндпоинт для получения транзакций конкретного пользователя."
# )
# async def get_user_transactions(
#     user_id: int,
#     current_user: MUser = Depends(get_current_user)
# ):
#     if current_user.id != user_id and not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Доступ запрещён"
#         )
#
#     transactions = await get_transactions_by_user(user_id=user_id)
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={"transactions": [t.model_dump() for t in transactions]}
#     )
