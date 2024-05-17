from abc import abstractmethod

from sqlalchemy import select

from exceptions.exceptions import DataNotFoundException, InvalidUserDataException
from models.user import User
from schemas.user_schema import UserSchema
from .repository import AbstractRepository, SQLAlchemyRepository
from db.db import async_session_maker


class AbstractUserRepository(AbstractRepository):
    @abstractmethod
    async def get_by_email(self, email: str) -> UserSchema:
        raise NotImplementedError
    

class UserRepository(SQLAlchemyRepository, AbstractUserRepository):
    model = User

    async def get_by_email(self, email: str) -> UserSchema:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.email == email)
            data = await session.execute(stmt)
            res = data.one_or_none()

            if not res:
                raise InvalidUserDataException()
            
            return res[0].to_read_model()
