from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
