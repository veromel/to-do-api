from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.models.task_status import TaskStatus


@dataclass
class Task:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    user_id: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    due_date: Optional[datetime] = None
