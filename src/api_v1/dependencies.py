from repositories.role_repository import RoleRepository
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from services.role_service import RoleService
from services.token_service import TokenService
from services.user_service import UserService


def role_service():
    return RoleService(RoleRepository)

def user_service():
    return UserService(UserRepository, RoleRepository)

def jwt_token_service():
    return TokenService(TokenRepository)
