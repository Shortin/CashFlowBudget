from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.future import select

from app.crud.financeCrud import *
from app.crud.usersCrud import *
from app.db.session import get_db
from app.schemas.financeSchemas import *

router = APIRouter()


# ------------------ Расходы (Expense) -------------------

# todo начать формировать нормалье запросы

# @router.post("/expenses", response_model=TransactionDetail, tags=["Expenses"])
# async def post_expense(expense: TransactionCreate):
#     """
#     Создает новый расход.
#
#     - **expense**: Данные о новом расходе, который будет создан.
#     """
#     return await create_expense_db(expense=expense)
#
#
# @router.get("/expenses/{expense_id}", response_model=TransactionDetail, tags=["Expenses"])
# async def get_expense_by_id(expense_id: int):
#     """
#     Получает расход по ID.
#
#     - **expense_id**: Уникальный идентификатор расхода.
#     """
#     db_expense = await get_expense_db(expense_id=expense_id)
#     if db_expense is None:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return db_expense
#
#
# @router.get("/expenses", response_model=list[TransactionDetail], tags=["Expenses"])
# async def get_expenses(skip: int = 0, limit: int = 100):
#     """
#     Получает список расходов.
#
#     - **skip**: Количество пропущенных расходов.
#     - **limit**: Количество расходов, которые будут возвращены.
#     """
#     return await get_expenses_db(skip=skip, limit=limit)
#
#
# @router.put("/expenses/{expense_id}", response_model=TransactionDetail, tags=["Expenses"])
# async def put_expense(expense_id: int, expense: TransactionUpdateBase):
#     """
#     Обновляет информацию о расходе по ID.
#
#     - **expense_id**: Уникальный идентификатор расхода.
#     - **expense**: Обновленные данные расхода.
#     """
#     db_expense = await update_expense_db(expense_id=expense_id, expense=expense)
#     if db_expense is None:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return db_expense
#
#
# @router.delete("/expenses/{expense_id}", response_model=TransactionDetail, tags=["Expenses"])
# async def delete_expense(expense_id: int):
#     """
#     Удаляет расход по ID.
#
#     - **expense_id**: Уникальный идентификатор расхода.
#     """
#     db_expense = await delete_expense_db(expense_id=expense_id)
#     if db_expense is None:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return db_expense
#
#
# # ------------------ Доходы (Income) -------------------
#
# @router.post("/incomes", response_model=TransactionDetail, tags=["Incomes"])
# async def post_income(income: IncomeCreate):
#     """
#     Создает новый доход.
#
#     - **income**: Данные о новом доходе, который будет создан.
#     """
#     return await create_income_db(income=income)
#
#
# @router.get("/incomes/{income_id}", response_model=TransactionDetail, tags=["Incomes"])
# async def get_income_by_id(income_id: int):
#     """
#     Получает доход по ID.
#
#     - **income_id**: Уникальный идентификатор дохода.
#     """
#     db_income = await get_income_db(income_id=income_id)
#     if db_income is None:
#         raise HTTPException(status_code=404, detail="Income not found")
#     return db_income
#
#
# @router.get("/incomes", response_model=list[TransactionBase], tags=["Incomes"])
# async def get_incomes(skip: int = 0, limit: int = 100):
#     """
#     Получает список доходов.
#
#     - **skip**: Количество пропущенных доходов.
#     - **limit**: Количество доходов, которые будут возвращены.
#     """
#     async for session in get_db():
#         db_incomes = await session.execute(select(Income).offset(skip).limit(limit))
#         db_incomes = db_incomes.scalars().all()
#         if not db_incomes:
#             raise HTTPException(status_code=404, detail="Incomes not found")
#         return db_incomes
#
#
# @router.put("/incomes/{income_id}", response_model=TransactionDetail, tags=["Incomes"])
# async def put_income(income_id: int, income: TransactionUpdateBase):
#     """
#     Обновляет информацию о доходе по ID.
#
#     - **income_id**: Уникальный идентификатор дохода.
#     - **income**: Обновленные данные дохода.
#     """
#     db_income = await update_income_db(income_id=income_id, income=income)
#     if db_income is None:
#         raise HTTPException(status_code=404, detail="Income not found")
#     return db_income
#
#
# @router.delete("/incomes/{income_id}", response_model=TransactionDetail, tags=["Incomes"])
# async def delete_income(income_id: int):
#     """
#     Удаляет доход по ID.
#
#     - **income_id**: Уникальный идентификатор дохода.
#     """
#     db_income = await delete_income_db(income_id=income_id)
#     if db_income is None:
#         raise HTTPException(status_code=404, detail="Income not found")
#     return db_income
