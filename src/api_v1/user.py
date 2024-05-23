from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from jwt import InvalidTokenError

from api_v1.dependencies import jwt_token_service, user_service
from api_v1.jwt_auth.helpers import create_access_token, create_refresh_token
from exceptions.exceptions import InvalidTokenException
from schemas.user_schema import IssuedJWTTokenSchema, JWTUserSchema, LoginUserSchema, RegisterUserSchema, TokenInfoSchema, UpdateUserDataSchema
from services.token_service import TokenService
from services.user_service import UserService
from utils.auth import decode_jwt
from api_v1.jwt_auth.validations import get_current_auth_payload_for_refresh


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/register")
async def register_user(
    data: RegisterUserSchema,
    user_service: UserService =Depends(user_service)
):
    user_id = await user_service.create(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"user_id": user_id}
    )


@auth_router.post("/login")
async def login_user(
    data: LoginUserSchema,
    user_service: UserService =Depends(user_service),
    jwt_token_service: TokenService =Depends(jwt_token_service)
):
    jwt_payload = await user_service.authenticate_user(data)
    access_token = create_access_token(jwt_payload)
    refresh_token, token_jti = create_refresh_token(jwt_payload)

    token_schema = IssuedJWTTokenSchema(
        id=token_jti,
        user_id=jwt_payload.id
    )
    await jwt_token_service.create(token_schema)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
    

@auth_router.patch("/update-user")
async def update_user(
    data: UpdateUserDataSchema,
    user_service: UserService =Depends(user_service)
):
    try:
        payload = decode_jwt(data.token)
        
    except InvalidTokenError:
        raise InvalidTokenException()
    
    await user_service.update_user(payload.get("sub"), data.password, data.action)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User updated"}
    )


@auth_router.post("/refresh-token")
async def refresh_token(
    payload : dict = Depends(get_current_auth_payload_for_refresh),
    jwt_token_service: TokenService =Depends(jwt_token_service),
    user_service: UserService =Depends(user_service)
) -> TokenInfoSchema:
    user = await user_service.get_by_id(payload.get("sub"))

    jwt_payload = JWTUserSchema(
        id=user.id,
        username=user.username,
        role=user.role
    )

    access_token = create_access_token(jwt_payload)
    refresh_token, token_jti = create_refresh_token(jwt_payload)

    await jwt_token_service.refresh(payload.get("jti"), token_jti, user.id)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
