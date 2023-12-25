from src import schemas, models
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_ as _or
from fastapi import status, HTTPException


# Expense CRUD functions
def create_expense(
    expense: schemas.ExpenseBase, db: Session, user: schemas.UserRead
) -> schemas.ExpenseRead:
    expense_obj = models.Expense(**expense.model_dump(), user_id=user.id)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return jsonable_encoder(expense_obj)


def get_expenses(
    db: Session,
    user: schemas.UserRead,
    query: str = None,
) -> list[schemas.ExpenseRead]:
    if query:
        return db.query(models.Expense).filter(
            _or(
                models.Expense.description.contains(query),
                models.Expense.category.contains(query),
            ),
            models.Expense.user_id == user.id,
        )
    return db.query(models.Expense).filter(models.Expense.user_id == user.id)


def get_expense_by_id(
    expense_id: int, db: Session, user: schemas.UserRead
) -> schemas.ExpenseRead:
    expense_obj = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.user_id == user.id)
        .first()
    )
    if not expense_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id={expense_id} for user=@{user.username} not found",
        )
    return expense_obj


def update_expense(
    expense_id: int, expense: schemas.ExpenseUpdate, db: Session, user: schemas.UserRead
) -> schemas.ExpenseRead:
    expense_obj = get_expense_by_id(expense_id, db, user)
    if expense_obj:
        for key, value in expense.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        ).items():
            if key in expense.model_dump().keys():
                setattr(expense_obj, key, value)
        db.commit()
        db.refresh(expense_obj)
    return jsonable_encoder(expense_obj)


# Income CRUD functions
def create_income_record(
    income: schemas.IncomeBase, db: Session, user: schemas.UserRead
) -> schemas.IncomeRead:
    income_obj = models.Income(**income.model_dump(), user_id=user.id)
    db.add(income_obj)
    db.commit()
    db.refresh(income_obj)
    return jsonable_encoder(income_obj)


def get_income_records(
    db: Session, user: schemas.UserRead, query: str = None
) -> list[schemas.ExpenseRead]:
    if query:
        return db.query(models.Income).filter(
            _or(
                models.Income.description.contains(query),
                models.Income.source.contains(query),
            ),
            models.Income.user_id == user.id,
        )
    return db.query(models.Income).filter(models.Income.user_id == user.id)


def get_income_record_by_id(
    income_id: int, db: Session, user: schemas.UserRead
) -> schemas.ExpenseRead:
    income_obj = (
        db.query(models.Income)
        .filter(models.Income.user_id == user.id, models.Income.id == income_id)
        .first()
    )
    if not income_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id={income_id} for user=@{user.username} not found",
        )
    return income_obj


def update_income_record(
    income_id: int, income: schemas.IncomeUpdate, db: Session, user: schemas.UserRead
) -> schemas.IncomeRead:
    income_obj = get_income_record_by_id(income_id, db, user)
    if income_obj:
        for key, value in income.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        ).items():
            if key in income.model_dump().keys():
                setattr(income_obj, key, value)
        db.commit()
        db.refresh(income_obj)
    return jsonable_encoder(income_obj)


# User CRUD functions
async def fetch_user_by_name(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found!")
    return user
