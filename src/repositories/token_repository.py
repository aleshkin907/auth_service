from abc import ABC, abstractmethod
import uuid

from db.db import async_session_maker
from models.issued_jwt import IssuedJWTToken
from schemas.user_schema import IssuedJWTTokenSchema



class AbstractTokenRepository:
    @abstractmethod
    async def create_or_update(self, token_schema: IssuedJWTTokenSchema, token_jti: uuid.UUID = None) -> None:
        raise NotImplementedError
    

class TokenRepository(AbstractTokenRepository):
    model = IssuedJWTToken

    async def create_or_update(self, token_schema: IssuedJWTTokenSchema, token_jti: uuid.UUID = None) -> None:
        pass
    