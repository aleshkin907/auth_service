from api_v1.jwt_auth.helpers import create_access_token
from exceptions.exceptions import InvalidUserDataException
from models.user import User
from repositories.user_repository import AbstractUserRepository, UserRepository
from schemas.email_schema import EmailSchema
from schemas.user_schema import JWTUserSchema, LoginUserSchema, RegisterUserSchema, UserSchema
from services.email_service import EmailSender
from utils.auth import hash_password, validate_password
from utils.consts import USER_ROLE_NAME, VERIFICATION_PARAM


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository: UserRepository = user_repository()

    async def create(self, user: RegisterUserSchema) -> int:
        user_dict = user.model_dump()
        hashed_password = hash_password(user.password)
        user_dict["hash_password"] = hashed_password
        del user_dict["password"]

        user_model: User = await self.user_repository.create(user_dict)

        jwt_payload_schema = JWTUserSchema(
            id=user_model.id,
            username=user_model.username,
            role=user_model.role
        )
        token = create_access_token(jwt_payload_schema)

        email_data = EmailSchema(email_type=VERIFICATION_PARAM, username=user_model.username, email=user_model.email, token=token)

        email_sender = EmailSender(email_data)
        await email_sender.send_email()

        return user_model.id
    
    async def update_user(self, user_id: int, password: str | None, action: str) -> None:
        if action == VERIFICATION_PARAM:
            await self.user_repository.update(user_id, {"is_active": True})
        else:
            new_password = hash_password(password)
            await self.user_repository.update(user_id, {"hash_password": new_password})

    async def authenticate_user(self, data: LoginUserSchema) -> JWTUserSchema:
        user_model: User = await self.user_repository.get_by_email(data.email)

        if not validate_password(data.password, user_model.hash_password) or user_model.is_active == False:
            raise InvalidUserDataException()

        return JWTUserSchema(
            id=user_model.id,
            username=user_model.username,
            role=user_model.role
        )
    
    async def get_by_id(self, id: int) -> UserSchema:
        user = await self.user_repository.get_one(id)
        return user
