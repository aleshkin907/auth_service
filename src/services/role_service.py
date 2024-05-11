from typing import List
from repositories.role_repository import AbstractRoleRepository
from schemas.role_schema import RoleSchema, RequestRoleSchema


class RoleService:
    def __init__(self, repository: AbstractRoleRepository) -> None:
        self.repository: AbstractRoleRepository = repository()
    
    async def create(self, role: RequestRoleSchema) -> int:
        role_dict = role.model_dump()
        role_id = await self.repository.create(role_dict)
        return role_id
    
    async def get_one(self, id: int) -> RoleSchema:
        role = await self.repository.get_one(id)
        return role
    
    async def get_all(self) -> List[RoleSchema]:
        roles = await self.repository.get_all()
        return roles
    
    async def update(self, id: int, role: RequestRoleSchema) -> RoleSchema:
        role_dict = role.model_dump()
        role_id = await self.repository.update(id, role_dict)
        return role_id
    
    async def delete(self, id: int) -> None:
        await self.repository.delete(id)
