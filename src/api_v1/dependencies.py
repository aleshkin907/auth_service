from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from services.role_service import RoleService
from services.user_service import UserService


def role_service():
    return RoleService(RoleRepository)

def user_service():
    return UserService(UserRepository, RoleRepository)
