from api_v1.jwt_auth.helpers import create_access_token
from exceptions.exceptions import InvalidUserDataException
from repositories.role_repository import AbstractRoleRepository, RoleRepository
from repositories.user_repository import AbstractUserRepository, UserRepository
from schemas.email_schema import EmailSchema
from schemas.user_schema import JWTUserSchema, LoginUserSchema, RegisterUserSchema
from services.email_service import EmailSender
from utils.auth import hash_password, validate_password
from utils.consts import USER_ROLE_NAME, VERIFICATION_PARAM


class UserService:
    def __init__(self, user_repository: AbstractUserRepository, role_repository: AbstractRoleRepository):
        self.user_repository: UserRepository = user_repository()
        self.role_repository: RoleRepository = role_repository()

    async def create(self, user: RegisterUserSchema) -> int:
        user_dict = user.model_dump()
        hashed_password = hash_password(user.password)
        user_dict["hash_password"] = hashed_password
        del user_dict["password"]

        role_id = await self.role_repository.get_by_name(USER_ROLE_NAME)
        user_dict["role_id"] = role_id

        user_id = await self.user_repository.create(user_dict)
        user = await self.user_repository.get_one(user_id)

        jwt_payload_schema = JWTUserSchema(
            id=user.id,
            username=user.username,
            role=USER_ROLE_NAME
        )
        token = create_access_token(jwt_payload_schema)

        email_data = EmailSchema(email_type=VERIFICATION_PARAM, username=user.username, email=user.email, token=token)

        email_sender = EmailSender(email_data)
        await email_sender.send_email()

        return user_id
    
    async def update_user(self, user_id: int, password: str | None, action: str) -> None:
        if action == VERIFICATION_PARAM:
            await self.user_repository.update(user_id, {"is_active": True})
        else:
            new_password = hash_password(password)
            await self.user_repository.update(user_id, {"hash_password": new_password})

    async def authenticate_user(self, data: LoginUserSchema) -> JWTUserSchema:
        user_db = await self.user_repository.get_by_email(data.email)
        role = await self.role_repository.get_one(user_db.role_id)

        if not validate_password(data.password, user_db.hash_password) or user_db.is_active == False:
            raise InvalidUserDataException()
        
        return JWTUserSchema(
            id=user_db.id,
            username=user_db.username,
            role=role.name
        )
    