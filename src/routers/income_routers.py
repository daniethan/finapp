from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src import schemas, dbconfig, crud
from typing import Annotated
from src.helpers import get_current_active_user


router = APIRouter(prefix="/incomes", tags=["Income"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.IncomeRead],
)
async def get_all_incomes(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    query: str = None,
):
    return crud.get_income_records(db, current_user, query)


@router.get(
    "/{income_id}",
    tags=["Income"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.IncomeRead,
)
async def get_income(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    income_id: int,
):
    return crud.get_income_record_by_id(income_id, db, current_user)


@router.post(
    "/",
    tags=["Income"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.IncomeRead,
)
async def record_income(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    income: schemas.IncomeBase,
):
    return crud.create_income_record(income, db, current_user)


@router.patch(
    "/{income_id}",
    tags=["Income"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.IncomeRead,
)
async def edit_income_record(
    current_user: Annotated[schemas.UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(dbconfig.get_db_session)],
    income_id: int,
    income: schemas.IncomeUpdate,
):
    return crud.update_income_record(income_id, income, db, current_user)
