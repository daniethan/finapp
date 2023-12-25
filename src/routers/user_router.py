from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from src.crud import fetch_user_by_name
from src.helpers import (
    PasswordHandler,
    TokenHandler,
    authenticate_user,
    get_current_active_user,
)
from src.models import User
from src.schemas import Token, UserCreate, UserRead
from sqlalchemy.orm import Session
from src.dbconfig import get_db_session


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_new_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db_session)]
) -> UserRead:
    user_obj = User(**user.model_dump())
    user_obj.password = PasswordHandler.get_password_hash(user_obj.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@router.post("/token", response_model=Token)
async def login_for_access_token(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db_session)],
):
    user = await authenticate_user(
        username=user_data.username, password=user_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    claims = dict(sub=user.username)
    access_token = TokenHandler.create_access_token(data=claims)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def get_logged_in_user(
    current_user: Annotated[UserRead, Depends(get_current_active_user)]
):
    return current_user


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def fetch_all_users(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db_session)],
):
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed!"
        )
    users = db.query(User).all()
    return users


@router.delete("/{username}", status_code=status.HTTP_200_OK)
async def deactivate_user(
    username: str,
    db: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    user = await fetch_user_by_name(username, db)
    user.disabled = True
    db.commit()
    return {"msg": f"{username} has been deactivated by {current_user.username}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
