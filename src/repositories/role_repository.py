from abc import ABC, abstractmethod

from sqlalchemy import select
from db.db import async_session_maker

from exceptions.exceptions import DataNotFoundException
from models.role import Role
from .repository import AbstractRepository, SQLAlchemyRepository


class AbstractRoleRepository(AbstractRepository):
    @abstractmethod
    async def get_by_name(self, name: str) -> int:
        raise NotImplementedError
    

class RoleRepository(SQLAlchemyRepository, AbstractRoleRepository):
    model = Role

    async def get_by_name(self, name: str) -> int:
        async with async_session_maker() as session:
            stmt = select(self.model.id).where(self.model.name == name)
            data = await session.execute(stmt)
            res = data.scalars().first()
            
            if not res:
                raise DataNotFoundException
            
            return res
    