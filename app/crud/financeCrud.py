from sqlalchemy.orm import Session

from app.db.models.usersModel import *
from app.schemas.financeSchemas import ExpenseCreate, ExpenseUpdate, IncomeCreate, IncomeUpdate
from app.schemas.usersSchemas import *
from app.utils.crud_utils import create_entity, get_entity, get_entities, update_entity, delete_entity


# CRUD для Expense
def create_expense_db(db: Session, expense: ExpenseCreate):
    return create_entity(
        db,
        Expense,
        amount=expense.amount,
        description=expense.description,
        user_id=expense.user_id,
        created_at=expense.created_at if expense.created_at is not None else datetime.now(timezone.utc)
    )


def get_expense_db(db: Session, expense_id: int):
    return get_entity(db, Expense, expense_id)


def get_expenses_db(db: Session, skip: int = 0, limit: int = 100):
    return get_entities(db, Expense, skip, limit)


def update_expense_db(db: Session, expense_id: int, expense: ExpenseUpdate):
    return update_entity(db, Expense, expense_id, expense.model_dump(exclude_unset=True))


def delete_expense_db(db: Session, expense_id: int):
    return delete_entity(db, Expense, expense_id)


# CRUD для Income
def create_income_db(db: Session, income: IncomeCreate):
    return create_entity(
        db,
        Income,
        amount=income.amount,
        description=income.description,
        user_id=income.user_id,
        created_at=income.created_at if income.created_at is not None else datetime.now(timezone.utc)
    )


def get_income_db(db: Session, income_id: int):
    return get_entity(db, Income, income_id)


def get_incomes_db(db: Session, skip: int = 0, limit: int = 100):
    return get_entities(db, Income, skip, limit)


def update_income_db(db: Session, income_id: int, income: IncomeUpdate):
    return update_entity(db, Income, income_id, income.model_dump(exclude_unset=True))


def delete_income_db(db: Session, income_id: int):
    return delete_entity(db, Income, income_id)