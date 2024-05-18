import uuid

from repositories.token_repository import AbstractTokenRepository
from schemas.user_schema import IssuedJWTTokenSchema


class TokenService:
    def __init__(self, repository: AbstractTokenRepository) -> None:
        self.repository: AbstractTokenRepository = repository()
    
    async def create_or_update(self, token_schema: IssuedJWTTokenSchema, token_jti: uuid.UUID = None) -> None:
        token_dict = token_schema.model_dump()
        await self.repository.create_or_update(token_dict)
    