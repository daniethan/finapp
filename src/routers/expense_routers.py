from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src import schemas, dbconfig, crud
from typing import Annotated, List

from src.helpers import get_current_active_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ExpenseRead],
)
async def get_or_search_all_expenses(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    query: str = None,
):
    return crud.get_expenses(db, current_user, query)


@router.get(
    "/{expense_id}",
    tags=["Expenses"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ExpenseRead,
)
async def get_expense(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    expense_id: int,
):
    return crud.get_expense_by_id(expense_id, db, current_user)


@router.post(
    "/",
    tags=["Expenses"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ExpenseRead,
)
async def create_expense(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    expense: schemas.ExpenseBase,
):
    return crud.create_expense(expense, db, current_user)


@router.patch(
    "/{expense_id}",
    tags=["Expenses"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ExpenseRead,
)
async def edit_expense(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    expense_id: int,
    expense: schemas.ExpenseUpdate,
):
    return crud.update_expense(expense_id, expense, db, current_user)
