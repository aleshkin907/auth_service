from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from services.token_service import TokenService
from services.user_service import UserService


def user_service():
    return UserService(UserRepository)

def jwt_token_service():
    return TokenService(TokenRepository)
