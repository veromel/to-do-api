from datetime import datetime
from typing import List, Optional, Dict, Any
import inject

from src.domain.models.task import Task, TaskStatus
from src.domain.ports.task_repository import TaskRepository
from src.domain.ports.user_repository import UserRepository


class TaskService:

    @inject.autoparams()
    def __init__(
        self, task_repository: TaskRepository, user_repository: UserRepository
    ):
        self.task_repository = task_repository
        self.user_repository = user_repository

    async def create_task(
        self,
        user_id: int,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING,
        due_date: Optional[datetime] = None,
    ) -> Task:

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        if due_date and due_date < datetime.now() and status != TaskStatus.COMPLETED:
            raise ValueError(
                "La fecha de vencimiento no puede ser en el pasado para tareas no completadas"
            )

        task = Task(
            title=title,
            description=description or "",
            status=status,
            user_id=user_id,
            due_date=due_date,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.task_repository.create(task)

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return await self.task_repository.get_by_id(task_id)

    async def get_user_tasks(
        self,
        user_id: int,
        status: Optional[TaskStatus] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        # Crear un diccionario con los filtros no nulos
        filters = {
            "user_id": user_id,
            "skip": skip,
            "limit": limit
        }
        
        # Añadir filtros opcionales si no son None
        if status is not None:
            filters["status"] = status
            
        if due_date_from is not None:
            filters["due_date_from"] = due_date_from
            
        if due_date_to is not None:
            filters["due_date_to"] = due_date_to

        return await self.task_repository.get_all(**filters)

    async def update_task(self, task_id: int, **kwargs) -> Task:

        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"No existe una tarea con el ID {task_id}")

        if not kwargs:
            return existing_task

        if "due_date" in kwargs and kwargs["due_date"]:
            due_date = kwargs["due_date"]
            new_status = kwargs.get("status", existing_task.status)

            if due_date < datetime.now() and new_status != TaskStatus.COMPLETED:
                raise ValueError(
                    "La fecha de vencimiento no puede ser en el pasado para tareas no completadas"
                )

        for field, value in kwargs.items():
            setattr(existing_task, field, value)

        existing_task.updated_at = datetime.now()

        return await self.task_repository.update(existing_task)

    async def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        return await self.update_task(task_id=task_id, status=status)

    async def delete_task(self, task_id: int) -> bool:
        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"No existe una tarea con el ID {task_id}")

        return await self.task_repository.delete(task_id)
