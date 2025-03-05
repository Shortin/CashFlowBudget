from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from starlette import status

from app.db.models.financeModel import MTransaction
from app.db.models.usersModel import MUser
from app.schemas.financesSchemas import STransactionPublic, STransactionCreate
from app.schemas.usersSchemas import SUserPublic
from app.service.financesService import get_transactions, post_transaction
from app.service.securityService import get_current_user

router = APIRouter(prefix='/finances', tags=['Finances'])


@router.get(
    "/get_transaction_for_period",
    summary="Get all transactions for the selected period",
    response_model=List[STransactionPublic]
)
async def get_transactions_for_period_endpoint(
        start_date: datetime = Query(..., description="Дата начала периода (обязательное поле)"),
        end_date: datetime = Query(default=datetime.now(), description="Дата окончания периода (обязательное поле)"),
        current_user: MUser = Depends(get_current_user),
):
    """
    Возвращает все транзакции текущего пользователя за указанный период.

    - **start_date**: Дата начала периода (обязательное поле)
    - **end_date**: Дата окончания периода (обязательное поле, не может быть меньше start_date)
    """
    if not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Both dates must be indicated")

    if end_date < start_date:
        raise HTTPException(status_code=400, detail="The end date cannot be less than the start date")

    return await get_transactions(current_user.id, start_date, end_date)


@router.post("/post_transaction",
             summary="Добавить новую транзакцию",
             response_model=STransactionPublic
             )
async def post_transaction_endpoint(
        transaction_data: STransactionCreate,
        current_user: MUser = Depends(get_current_user),
):
    """
    Добавляет новую транзакцию для текущего пользователя.

    - **amount**: сумма транзакции (обязательно)
    - **description**: описание (необязательно)
    - **is_income**: доход или расход (обязательно)
    """

    new_transaction = MTransaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        is_income=transaction_data.is_income,
        created_at=datetime.now(timezone.utc),  # Текущее время
        user_id=current_user.id # Используем данные текущего пользователя
    )

    return await post_transaction(new_transaction)