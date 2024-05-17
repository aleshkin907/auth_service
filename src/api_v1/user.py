from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from jwt import InvalidTokenError

from api_v1.dependencies import user_service
from api_v1.jwt_auth.helpers import create_access_token, create_refresh_token
from exceptions.exceptions import InvalidTokenException
from schemas.user_schema import LoginUserSchema, RegisterUserSchema, TokenInfoSchema, UpdateUserDataSchema
from services.user_service import UserService
from utils.auth import decode_jwt


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
    user_service: UserService =Depends(user_service)
):
    jwt_payload = await user_service.authenticate_user(data)
    access_token = create_access_token(jwt_payload)
    refresh_token = create_refresh_token(jwt_payload)

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
