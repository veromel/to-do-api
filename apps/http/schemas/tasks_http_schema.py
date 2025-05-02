from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from src.domain.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(
        ..., description="Título de la tarea", min_length=1, max_length=100
    )
    description: Optional[str] = Field(None, description="Descripción de la tarea")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Estado de la tarea")
    due_date: Optional[datetime] = Field(None, description="Fecha de vencimiento")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None, description="Título de la tarea", min_length=1, max_length=100
    )
    description: Optional[str] = Field(None, description="Descripción de la tarea")
    status: Optional[TaskStatus] = Field(None, description="Estado de la tarea")
    due_date: Optional[datetime] = Field(None, description="Fecha de vencimiento")


class TaskStatusUpdate(BaseModel):
    status: TaskStatus = Field(..., description="Estado de la tarea")


class Task(TaskBase):
    id: int = Field(..., description="ID de la tarea")
    user_id: int = Field(..., description="ID del usuario propietario")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    total: int = Field(..., description="Número total de tareas")
    items: List[Task] = Field(..., description="Lista de tareas")
