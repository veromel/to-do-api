from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User as UserEntity
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.schemas.user_schema import UserSchema


class SQLAlchemyUserRepository(UserRepository):
    """
    Adaptador del repositorio de usuarios con SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserEntity) -> UserEntity:
        db_user = UserSchema.from_domain(user)

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return UserSchema.to_domain(db_user)

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:

        result = await self.session.execute(
            select(UserSchema).where(UserSchema.id == user_id)
        )
        db_user = result.scalars().first()

        if db_user is None:
            return None

        return UserSchema.to_domain(db_user)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:

        result = await self.session.execute(
            select(UserSchema).where(UserSchema.username == username)
        )
        db_user = result.scalars().first()

        if db_user is None:
            return None

        return UserSchema.to_domain(db_user)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:

        result = await self.session.execute(
            select(UserSchema).where(UserSchema.email == email)
        )
        db_user = result.scalars().first()

        if db_user is None:
            return None

        return UserSchema.to_domain(db_user)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:

        result = await self.session.execute(
            select(UserSchema).offset(skip).limit(limit)
        )
        db_users = result.scalars().all()

        return [UserSchema.to_domain(db_user) for db_user in db_users]

    async def update(self, user: UserEntity) -> UserEntity:

        db_user = await self.session.get(UserSchema, user.id)
        if db_user is None:
            raise ValueError(f"No existe un usuario con el ID {user.id}")

        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.updated_at = user.updated_at

        await self.session.commit()
        await self.session.refresh(db_user)

        return UserSchema.to_domain(db_user)

    async def delete(self, user_id: int) -> bool:

        db_user = await self.session.get(UserSchema, user_id)
        if db_user is None:
            return False

        await self.session.delete(db_user)
        await self.session.commit()

        return True
