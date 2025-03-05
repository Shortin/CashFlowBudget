from datetime import datetime
from typing import Optional, List, Type

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.financeModel import MTransaction
from app.db.session import get_sessions
from app.schemas.financesSchemas import STransactionPublic
from app.schemas.usersSchemas import SUserPublic


class QueryBuilder:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session
        self.filters = []
        self.or_filters = []

    def filter_by(self, **kwargs):
        """Добавляет фильтры к запросу, игнорируя те, что равны None"""
        for key, value in kwargs.items():
            if value is not None:
                self.filters.append(getattr(self.model, key) == value)
        return self

    async def build(self):
        """Строит запрос с добавленными фильтрами и выполняет его с помощью сессии"""
        query = select(self.model)

        if self.filters:
            query = query.filter(and_(*self.filters))

        result = await self.session.execute(query)
        return result.scalars().all()


"""
    Finances
"""


async def get_transactions(
        user_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        is_income: Optional[bool] = None
) -> List[STransactionPublic]:
    """
    Получить список транзакций с возможностью фильтрации.

    :param session: Сессия БД.
    :param user_id: ID пользователя (если передан, фильтруем по нему).
    :param start_date: Дата начала периода (если передана, фильтруем).
    :param end_date: Дата окончания периода (если передана, фильтруем).
    :param min_amount: Минимальная сумма транзакции (если передана, фильтруем).
    :param max_amount: Максимальная сумма транзакции (если передана, фильтруем).
    :param is_income: Флаг дохода/расхода (если передан, фильтруем).
    :return: Список транзакций.
    """
    async with get_sessions() as session:
        query_builder = QueryBuilder(MTransaction, session)

        # Добавление фильтров через filter_by (только равенство)
        if user_id:
            query_builder.filter_by(user_id=user_id)
        if is_income is not None:
            query_builder.filter_by(is_income=is_income)

        # Добавление диапазонных фильтров вручную
        if start_date:
            query_builder.filters.append(MTransaction.created_at >= start_date)
        if end_date:
            query_builder.filters.append(MTransaction.created_at <= end_date)
        if min_amount is not None:
            query_builder.filters.append(MTransaction.amount >= min_amount)
        if max_amount is not None:
            query_builder.filters.append(MTransaction.amount <= max_amount)

        transactions = await query_builder.build()

    # Преобразуем список MTransaction в список STransactionPublic
    transaction_public_list = [
        STransactionPublic(
            id=transaction.id,
            amount=transaction.amount,
            description=transaction.description,
            is_income=transaction.is_income,
            created_at=transaction.created_at,
            user=SUserPublic(
                id=transaction.user.id,
                name=transaction.user.name,
                username=transaction.user.username,  # Если это поле есть
                role_name=transaction.user.role.name  # Если роль имеет поле name
            )
        ) for transaction in transactions
    ]

    return transaction_public_list

async def post_transaction(transaction_data: MTransaction) -> STransactionPublic:
    async with get_sessions() as session:
        try:
            # Добавляем транзакцию в сессию и коммитим
            session.add(transaction_data)
            await session.commit()
            await session.refresh(transaction_data)

            # Преобразуем MTransaction в STransactionPublic
            transaction_public = STransactionPublic(
                id=transaction_data.id,
                amount=transaction_data.amount,
                description=transaction_data.description,
                is_income=transaction_data.is_income,
                created_at=transaction_data.created_at,
                user=SUserPublic(
                    id=transaction_data.user.id,
                    name=transaction_data.user.name,
                    username=transaction_data.user.username,  # Если это поле есть
                    role_name=transaction_data.user.role.name  # Если роль имеет поле name
                )
            )

            return transaction_public  # Возвращаем полностью сформированный объект

        except IntegrityError as e:
            await session.rollback()
            raise e