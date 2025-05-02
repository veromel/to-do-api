from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.task import Task as TaskEntity, TaskStatus
from src.domain.ports.task_repository import TaskRepository
from src.infrastructure.schemas.task_schema import TaskSchema


class SQLAlchemyTaskRepository(TaskRepository):
    """
    Adaptador del repositorio de tareas con SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskEntity) -> TaskEntity:
        db_task = TaskSchema.from_domain(task)

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return TaskSchema.to_domain(db_task)

    async def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        result = await self.session.execute(
            select(TaskSchema).where(TaskSchema.id == task_id)
        )
        db_task = result.scalars().first()

        if db_task is None:
            return None

        return TaskSchema.to_domain(db_task)

    async def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> List[TaskEntity]:

        query = select(TaskSchema)
        filters = []

        # Mapeo de parámetros a condiciones de filtro
        filter_mapping = {
            'user_id': lambda value: TaskSchema.user_id == value,
            'status': lambda value: TaskSchema.status == value,
            'due_date_from': lambda value: TaskSchema.due_date >= value,
            'due_date_to': lambda value: TaskSchema.due_date <= value,
        }

        for key, value in kwargs.items():
            if key in filter_mapping and value is not None:
                filters.append(filter_mapping[key](value))
        
        if filters:
            query = query.where(and_(*filters))

        # Aplicar paginación
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        db_tasks = result.scalars().all()

        return [TaskSchema.to_domain(db_task) for db_task in db_tasks]

    async def update(self, task: TaskEntity) -> TaskEntity:
        db_task = await self.session.get(TaskSchema, task.id)
        if db_task is None:
            raise ValueError(f"No existe una tarea con el ID {task.id}")

        user_id = db_task.user_id
        created_at = db_task.created_at

        updated_schema = TaskSchema.from_domain(task)
        updated_schema.user_id = user_id
        updated_schema.created_at = created_at

        for key, value in updated_schema.__dict__.items():
            if key != "_sa_instance_state":  # Evitar atributo interno de SQLAlchemy
                setattr(db_task, key, value)

        await self.session.commit()
        await self.session.refresh(db_task)

        return TaskSchema.to_domain(db_task)

    async def delete(self, task_id: int) -> bool:
        db_task = await self.session.get(TaskSchema, task_id)
        if db_task is None:
            return False

        await self.session.delete(db_task)
        await self.session.commit()

        return True
