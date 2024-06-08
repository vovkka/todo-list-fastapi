from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.users.models import Users

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)


def authenticate_user(user: Users, password):
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return encoded_jwt
