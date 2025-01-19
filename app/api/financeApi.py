from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session  # noqa

from app.crud.financeCrud import *
from app.crud.usersCrud import *
from app.db.session import get_db
from app.schemas.financeSchemas import *

router = APIRouter()


# ------------------ Расходы (Expense) -------------------

@router.post("/expenses", response_model=ExpenseDetail)
def post_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense_db(db=db, expense=expense)


@router.get("/expenses/{expense_id}", response_model=ExpenseDetail)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    db_expense = get_expense_db(db=db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.get("/expenses", response_model=list[ExpenseDetail])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_expenses_db(db=db, skip=skip, limit=limit)


@router.put("/expenses/{expense_id}", response_model=ExpenseDetail)
def put_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = update_expense_db(db=db, expense_id=expense_id, expense=expense)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.delete("/expenses/{expense_id}", response_model=ExpenseDetail)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = delete_expense_db(db=db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


# ------------------ Доходы (Income) -------------------

@router.post("/incomes", response_model=IncomeDetail)
def post_income(income: IncomeCreate, db: Session = Depends(get_db)):
    return create_income_db(db=db, income=income)


@router.get("/incomes/{income_id}", response_model=IncomeDetail)
def get_income_by_id(income_id: int, db: Session = Depends(get_db)):
    db_income = get_income_db(db=db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income


@router.get("/incomes", response_model=list[IncomeBase])  # Используем схему IncomeBase
def get_incomes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Здесь нужно скорректировать логику запроса, если необходимо получить связанные данные (например, user_name)
    db_incomes = db.query(Income).offset(skip).limit(limit).all()
    if not db_incomes:
        raise HTTPException(status_code=404, detail="Incomes not found")
    return db_incomes


@router.put("/incomes/{income_id}", response_model=IncomeDetail)
def put_income(income_id: int, income: IncomeUpdate, db: Session = Depends(get_db)):
    db_income = update_income_db(db=db, income_id=income_id, income=income)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income


@router.delete("/incomes/{income_id}", response_model=IncomeDetail)
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = delete_income_db(db=db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income
