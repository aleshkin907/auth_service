from abc import ABC, abstractmethod
import uuid

from sqlalchemy import delete, insert, select, update

from db.db import async_session_maker
from exceptions.exceptions import ForbiddenException
from models.issued_jwt import IssuedJWTToken
from repositories.repository import SQLAlchemyRepository
from schemas.user_schema import IssuedJWTTokenSchema



class AbstractTokenRepository:
    @abstractmethod
    async def update_or_delete_all(self, id: uuid) -> None:
        raise NotImplementedError
    

class TokenRepository(SQLAlchemyRepository, AbstractTokenRepository):
    model = IssuedJWTToken

    async def update_or_delete_all(self, id: uuid, new_id: uuid, user_id: int) -> None:
        async with async_session_maker() as session:
            select_stmt = select(self.model).where(self.model.id == id)
            token = await session.execute(select_stmt)

            if not token.one_or_none():
                delete_stmt = delete(self.model).where(self.model.user_id == user_id)
                await session.execute(delete_stmt)
                await session.commit()
                raise ForbiddenException()
            
            update_stmt = update(self.model).where(self.model.id == id).values(id=new_id)
            await session.execute(update_stmt)
            await session.commit()
