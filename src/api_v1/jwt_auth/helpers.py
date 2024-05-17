from datetime import timedelta

from configs.config import settings
from schemas.user_schema import JWTUserSchema
from utils.auth import encode_jwt
from utils.consts import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )

def create_access_token(user: JWTUserSchema) -> str:
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "role": user.role,
    }
    token = create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload
    )
    return token


def create_refresh_token(user: JWTUserSchema) -> str:
    jwt_payload = {
        "sub": user.id,
    }
    token = create_jwt(
        token_type = REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.jwt.refresh_token_expire_days)
    )
    return token
