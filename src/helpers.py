from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.dbconfig import get_db_session
from src.models import User
from src.schemas import TokenData, UserRead, Token


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class PasswordHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(secret=password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str):
        return cls.pwd_context.verify(secret=password, hash=hashed_password)


class TokenHandler:
    DEFAULT_TOKEN_EXPIRY = timedelta(minutes=30)
    ALGORITHM = "HS256"
    SECRET_KEY = "1b449917b1924e105efb705ab22c53fb8329aed6c4b2c02d85a780a123b17e59"

    @staticmethod
    def create_access_token(data: dict, expiry: timedelta | None = None) -> str:
        data_to_encode = data.copy()
        expires_at = datetime.utcnow() + (
            timedelta(minutes=expiry) if expiry else TokenHandler.DEFAULT_TOKEN_EXPIRY
        )

        data_to_encode.update({"expires_at": jsonable_encoder(expires_at)})
        access_token = jwt.encode(
            claims=data_to_encode,
            key=TokenHandler.SECRET_KEY,
            algorithm=TokenHandler.ALGORITHM,
        )
        return access_token

    @staticmethod
    def decode_token(token: str) -> TokenData | None:
        token_data = None
        try:
            payload: dict = jwt.decode(
                token=token,
                key=TokenHandler.SECRET_KEY,
                algorithms=[TokenHandler.ALGORITHM],
            )
            token_data = TokenData(username=payload.get("sub"))
        except JWTError:
            raise credentials_exception
        return token_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_user_in_db(username: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return user


async def authenticate_user(
    username: str, password: str, db: Session
) -> UserRead | bool:
    user = get_user_in_db(username, db)
    if not user:
        return False
    if not PasswordHandler.verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    token: Token = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session),
) -> UserRead:
    token_data = TokenHandler.decode_token(token)
    if not token_data:
        raise credentials_exception
    user = get_user_in_db(token_data.username, db)
    if not user:
        raise credentials_exception
    user = UserRead(
        username=user.username,
        fullname=user.fullname,
        disabled=user.disabled,
        id=user.id,
    )
    return user


async def get_current_active_user(
    current_user: UserRead = Depends(get_current_user),
) -> UserRead:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user.",
        )
    return current_user

