from abc import ABC, abstractmethod
import re
from typing import Any, List

from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete, insert, select, update

from db.db import async_session_maker
from exceptions.exceptions import ConflictException, DataNotFoundException


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> int:
        raise NotImplementedError
    
    async def get_one(self, id: int) -> Any:
        raise NotImplementedError
    
    async def get_all(self) -> List[Any]:
        raise NotImplementedError
    
    async def update(self, id: int, data: dict) -> Any:
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create(self, data: dict) -> Any:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            try:
                res = await session.execute(stmt)
            except IntegrityError as e:
                pattern = r'\(([^)]+)\)'
                field = re.findall(pattern, str(e.orig))
                raise ConflictException(msg=field[0])
            
            await session.commit()
            return res.scalar_one()

    async def get_one(self, id: int) -> Any:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            data = await session.execute(stmt)
            res = data.one_or_none()

            if not res:
                raise DataNotFoundException
            
            return res[0].to_read_model()

    async def get_all(self) -> List[Any]:
        async with async_session_maker() as session:
            stmt = select(self.model).order_by(self.model.id.desc())
            data = await session.execute(stmt)
            res = [row[0].to_read_model() for row in data]

            if not res:
                raise DataNotFoundException
            
            return res
        
    async def update(self, id: int, data: dict) -> Any:
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
            res = await session.execute(stmt)
            updated_role = res.scalars().first()
            await session.commit()

            if not updated_role:
                raise DataNotFoundException
            
            return updated_role.to_read_model()
    
    async def delete(self, id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            res = await session.execute(stmt)

            if res.rowcount == 0:
                raise DataNotFoundException
            
            await session.commit()
