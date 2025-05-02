from datetime import datetime
from typing import List, Optional, Dict, Any
import inject

from src.domain.models.user import User
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.auth.jwt_auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from apps.http.schemas.users_http_schema import User as UserResponse, UserList, Token


class UserService:
    @inject.autoparams()
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, username: str, email: str, password: str) -> User:
        await self._check_unique_email(email)
        await self._check_unique_username(username)

        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.user_repository.create(user)

    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[Dict[str, str]]:
        user = await self.user_repository.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(data={"sub": user.username})

        return {"access_token": access_token, "token_type": "bearer"}

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repository.get_by_username(username)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repository.get_all(skip, limit)

    async def update_user(self, user_id: int, **kwargs) -> User:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        if not kwargs:
            return existing_user

        # Verificar y procesar cambios
        if "username" in kwargs and kwargs["username"] != existing_user.username:
            await self._check_unique_username(kwargs["username"], exclude_id=user_id)
            existing_user.username = kwargs["username"]

        if "email" in kwargs and kwargs["email"] != existing_user.email:
            await self._check_unique_email(kwargs["email"], exclude_id=user_id)
            existing_user.email = kwargs["email"]

        if "password" in kwargs and kwargs["password"]:
            existing_user.hashed_password = get_password_hash(kwargs["password"])

        existing_user.updated_at = datetime.now()

        return await self.user_repository.update(existing_user)

    async def delete_user(self, user_id: int) -> bool:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        return await self.user_repository.delete(user_id)

    async def _check_unique_email(
        self, email: str, exclude_id: Optional[int] = None
    ) -> None:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user and (exclude_id is None or existing_user.id != exclude_id):
            raise ValueError(f"Ya existe un usuario con el email {email}")

    async def _check_unique_username(
        self, username: str, exclude_id: Optional[int] = None
    ) -> None:
        existing_user = await self.user_repository.get_by_username(username)
        if existing_user and (exclude_id is None or existing_user.id != exclude_id):
            raise ValueError(f"Ya existe un usuario con el username {username}")
