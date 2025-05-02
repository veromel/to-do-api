import pytest
from faker import Faker

from src.domain.models.user import User
from src.domain.models.task import Task
from src.domain.models.task_status import TaskStatus

@pytest.fixture
def faker():
    return Faker()

@pytest.fixture
def user(faker):
    def _create_user(**kwargs):
        return User(
            id=kwargs.get("id") or faker.random_int(),
            username=kwargs.get("username") or faker.user_name(),
            email=kwargs.get("email") or faker.email(),
            hashed_password=kwargs.get("hashed_password") or faker.password(),
            created_at=kwargs.get("created_at") or faker.date_time(),
            updated_at=kwargs.get("updated_at") or faker.date_time(),
        )
    return _create_user

@pytest.fixture
def task(faker):
    def _create_task(**kwargs):
        return Task(
            id=kwargs.get("id") or faker.random_int(),
            title=kwargs.get("title") or faker.sentence(),
            description=kwargs.get("description") or faker.text(),
            status=kwargs.get("status") or faker.random_element(TaskStatus),
            due_date=kwargs.get("due_date") or faker.date_time(),
            created_at=kwargs.get("created_at") or faker.date_time(),
            updated_at=kwargs.get("updated_at") or faker.date_time(),
            user_id=kwargs.get("user_id") or faker.random_int()
        )
    return _create_task