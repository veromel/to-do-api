from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.domain.models.user import User as UserEntity
from src.infrastructure.database import Base


class UserSchema(Base):
    """Modelo tabla de usuarios."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relación con tasks
    tasks = relationship(
        "TaskSchema", back_populates="user", cascade="all, delete-orphan"
    )

    @staticmethod
    def to_domain(user_model) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    @staticmethod
    def from_domain(user_entity: UserEntity):
        return UserSchema(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            hashed_password=user_entity.hashed_password,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
        )
