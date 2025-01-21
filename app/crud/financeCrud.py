from app.db.models.usersModel import *
from app.schemas.financeSchemas import TransactionCreate, IncomeCreate, TransactionUpdateBase
from app.utils.crud_utils import create_entity, get_entity, get_entities, update_entity, delete_entity
from datetime import datetime, timezone

# Асинхронные CRUD для Expense

async def create_expense_db(expense: TransactionCreate):
    """
    Создает новый расход (Expense) в базе данных.

    - **db**: Асинхронная сессия базы данных.
    - **expense**: Данные расхода, которые необходимо сохранить.

    Возвращает созданный объект расхода.
    """
    return await create_entity(
        Expense,
        amount=expense.amount,
        description=expense.description,
        user_id=expense.user_id,
        created_at=expense.created_at if expense.created_at is not None else datetime.now(timezone.utc)
    )


async def get_expense_db(expense_id: int):
    """
    Получает расход (Expense) по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **expense_id**: Уникальный идентификатор расхода.

    Возвращает объект расхода или None, если расход не найден.
    """
    return await get_entity(Expense, expense_id)


async def get_expenses_db(skip: int = 0, limit: int = 100):
    """
    Получает список расходов с возможностью пропуска и ограничения.

    - **db**: Асинхронная сессия базы данных.
    - **skip**: Количество расходов для пропуска (по умолчанию 0).
    - **limit**: Количество расходов для возврата (по умолчанию 100).

    Возвращает список расходов.
    """
    return await get_entities(Expense, skip, limit)


async def update_expense_db(expense_id: int, expense: TransactionUpdateBase):
    """
    Обновляет данные расхода по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **expense_id**: Уникальный идентификатор расхода.
    - **expense**: Данные для обновления расхода.

    Возвращает обновленный объект расхода или None, если расход не найден.
    """
    return await update_entity(Expense, expense_id, expense.model_dump(exclude_unset=True))


async def delete_expense_db(expense_id: int):
    """
    Удаляет расход по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **expense_id**: Уникальный идентификатор расхода.

    Возвращает удаленный объект расхода или None, если расход не найден.
    """
    return await delete_entity(Expense, expense_id)


# Асинхронные CRUD для Income

async def create_income_db(income: IncomeCreate):
    """
    Создает новый доход (Income) в базе данных.

    - **db**: Асинхронная сессия базы данных.
    - **income**: Данные дохода, которые необходимо сохранить.

    Возвращает созданный объект дохода.
    """
    return await create_entity(
        Income,
        amount=income.amount,
        description=income.description,
        user_id=income.user_id,
        created_at=income.created_at if income.created_at is not None else datetime.now(timezone.utc)
    )


async def get_income_db(income_id: int):
    """
    Получает доход (Income) по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **income_id**: Уникальный идентификатор дохода.

    Возвращает объект дохода или None, если доход не найден.
    """
    return await get_entity(Income, income_id)


async def get_incomes_db(skip: int = 0, limit: int = 100):
    """
    Получает список доходов с возможностью пропуска и ограничения.

    - **db**: Асинхронная сессия базы данных.
    - **skip**: Количество доходов для пропуска (по умолчанию 0).
    - **limit**: Количество доходов для возврата (по умолчанию 100).

    Возвращает список доходов.
    """
    return await get_entities(Income, skip, limit)


async def update_income_db(income_id: int, income: TransactionUpdateBase):
    """
    Обновляет данные дохода по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **income_id**: Уникальный идентификатор дохода.
    - **income**: Данные для обновления дохода.

    Возвращает обновленный объект дохода или None, если доход не найден.
    """
    return await update_entity(Income, income_id, income.model_dump(exclude_unset=True))


async def delete_income_db(income_id: int):
    """
    Удаляет доход по уникальному идентификатору.

    - **db**: Асинхронная сессия базы данных.
    - **income_id**: Уникальный идентификатор дохода.

    Возвращает удаленный объект дохода или None, если доход не найден.
    """
    return await delete_entity(Income, income_id)
