from .role import role_router
from .user import auth_router


all_routers = [
    role_router,
    auth_router
]
