from repositories.role_repository import RoleRepository
from services.role_service import RoleService


def role_service():
    return RoleService(RoleRepository)
