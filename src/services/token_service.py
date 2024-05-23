import uuid

from repositories.token_repository import TokenRepository
from schemas.user_schema import IssuedJWTTokenSchema


class TokenService:
    def __init__(self, repository: TokenRepository) -> None:
        self.repository: TokenRepository = repository()
    
    async def create(self, token_schema: IssuedJWTTokenSchema) -> None:
        token_dict = token_schema.model_dump()
        await self.repository.create(token_dict)

    async def refresh(self, id: uuid, new_id: uuid, user_id: int) -> None:
        await self.repository.update_or_delete_all(id, new_id, user_id)
    