from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from src.domain.models.task import Task as TaskEntity, TaskStatus
from src.infrastructure.database import Base


class TaskSchema(Base):
    """Modelo tabla de tareas."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relación con user
    user = relationship("UserSchema", back_populates="tasks")

    @staticmethod
    def to_domain(task_model) -> TaskEntity:
        return TaskEntity(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            status=task_model.status,
            user_id=task_model.user_id,
            created_at=task_model.created_at,
            due_date=task_model.due_date,
            updated_at=task_model.updated_at,
        )

    @staticmethod
    def from_domain(task_entity: TaskEntity):
        return TaskSchema(
            id=task_entity.id,
            title=task_entity.title,
            description=task_entity.description,
            status=task_entity.status,
            user_id=task_entity.user_id,
            created_at=task_entity.created_at,
            due_date=task_entity.due_date,
            updated_at=task_entity.updated_at,
        )
