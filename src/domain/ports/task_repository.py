from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Any

from src.domain.models.task import Task, TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        pass
