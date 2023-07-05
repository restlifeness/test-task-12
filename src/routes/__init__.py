
from .auth import auth_router
from .user import user_router
from .post import posts_router

__all__ = [
    'auth_router',
    'user_router',
    'posts_router',
]
