
from typing import Optional
from jwt import encode, decode, InvalidTokenError

from core.settings import get_settings


settings = get_settings()

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def create_token(
    payload: dict, 
    secret: Optional[str] = None,
) -> str:
    if not secret:
        secret = JWT_SECRET
    return encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_token(
    token: str, 
    secret: Optional[str] = None,
) -> Optional[dict]:
    if not secret:
        secret = JWT_SECRET
    try:
        return decode(token, secret, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError:
        return None
