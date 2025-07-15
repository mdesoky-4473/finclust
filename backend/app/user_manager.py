# app/user_manager.py
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models import User
from app.database import async_session
from fastapi_users import BaseUserManager, IntegerIDMixin
from app.schemas import UserCreate
from typing import AsyncGenerator

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    user_db_model = User
    reset_password_token_secret = "supersecret"
    verification_token_secret = "supersecret"

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.id} has registered.")

# ✅ FIXED: wrap session in SQLAlchemyUserDatabase
async def get_user_manager() -> AsyncGenerator[UserManager, None]:
    async with async_session() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        yield UserManager(user_db)
