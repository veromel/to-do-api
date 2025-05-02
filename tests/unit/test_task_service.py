import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime, timedelta

from src.application.services.task_service import TaskService
from src.domain.models.task import Task
from src.domain.models.task_status import TaskStatus


@pytest.mark.unit
class TestTaskService:
    def setup_method(self):
        self.task_repository = AsyncMock()
        self.user_repository = AsyncMock()

        self.service = TaskService(
            task_repository=self.task_repository, 
            user_repository=self.user_repository
        )
        

    @pytest.mark.asyncio
    async def test_create_task_successfully(self, faker, user):
        # Arrange
        test_user = user()
        title = faker.sentence()
        description = faker.text()
        status = TaskStatus.PENDING
        due_date = datetime.now() + timedelta(days=7)
        
        self.user_repository.get_by_id.return_value = test_user
        
        created_task = Task(
            id=faker.random_int(),
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            user_id=test_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.task_repository.create.return_value = created_task
        
        # Act
        result = await self.service.create_task(
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            user_id=test_user.id
        )
        
        # Assert
        assert result.title == title
        assert result.description == description
        assert result.status == status
        assert result.due_date == due_date
        assert result.user_id == test_user.id
        self.user_repository.get_by_id.assert_awaited_once_with(test_user.id)
        self.task_repository.create.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_task_with_past_due_date_raises_error(self, faker, user):
        # Arrange
        test_user = user()
        title = faker.sentence()
        description = faker.text()
        status = TaskStatus.PENDING
        due_date = datetime.now() - timedelta(days=1)  # Fecha pasada
        
        self.user_repository.get_by_id.return_value = test_user
        
        # Act & Assert
        with pytest.raises(ValueError, match="La fecha de vencimiento no puede ser en el pasado para tareas no completadas"):
            await self.service.create_task(
                title=title,
                description=description,
                status=status,
                due_date=due_date,
                user_id=test_user.id
            )
        
        self.user_repository.get_by_id.assert_awaited_once_with(test_user.id)
        self.task_repository.create.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_task_by_id(self, task, user):
        # Arrange
        test_task = task()
        task_id = test_task.id
        test_user = user()
        test_task.user_id = test_user.id
        
        self.task_repository.get_by_id.return_value = test_task
        
        # Act
        result = await self.service.get_task_by_id(task_id)
        
        # Assert
        assert result == test_task
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)

    @pytest.mark.asyncio
    async def test_get_user_tasks(self, task, user):
        # Arrange
        test_user = user()
        user_id = test_user.id
        
        test_tasks = [task() for _ in range(3)]
        for t in test_tasks:
            t.user_id = user_id
        
        self.user_repository.get_by_id.return_value = test_user
        self.task_repository.get_all.return_value = test_tasks
        
        # Act
        result = await self.service.get_user_tasks(user_id)
        
        # Assert
        assert result == test_tasks
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)
        self.task_repository.get_all.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_task_successfully(self, task, user):
        # Arrange
        test_task = task()
        task_id = test_task.id
        test_user = user()
        test_task.user_id = test_user.id
        
        new_title = "Nuevo título"
        new_description = "Nueva descripción"
        new_status = TaskStatus.IN_PROGRESS
        new_due_date = datetime.now() + timedelta(days=14)
        
        updated_task = Task(
            id=test_task.id,
            title=new_title,
            description=new_description,
            status=new_status,
            due_date=new_due_date,
            user_id=test_task.user_id,
            created_at=test_task.created_at,
            updated_at=datetime.now()
        )
        
        self.task_repository.get_by_id.return_value = test_task
        self.task_repository.update.return_value = updated_task
        
        # Act
        result = await self.service.update_task(
            task_id=task_id,
            title=new_title,
            description=new_description,
            status=new_status,
            due_date=new_due_date
        )
        
        # Assert
        assert result.title == new_title
        assert result.description == new_description
        assert result.status == new_status
        assert result.due_date == new_due_date
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, faker):
        # Arrange
        task_id = faker.random_int()
        new_title = "Nuevo título"
        
        self.task_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"No existe una tarea con el ID {task_id}"):
            await self.service.update_task(
                task_id=task_id,
                title=new_title
            )
        
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_task_with_past_due_date_raises_error(self, task):
        # Arrange
        test_task = task()
        task_id = test_task.id
        test_task.status = TaskStatus.PENDING
        
        past_due_date = datetime.now() - timedelta(days=1)
        
        self.task_repository.get_by_id.return_value = test_task
        
        # Act & Assert
        with pytest.raises(ValueError, match="La fecha de vencimiento no puede ser en el pasado para tareas no completadas"):
            await self.service.update_task(
                task_id=task_id,
                due_date=past_due_date
            )
        
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_task_status_successfully(self, task):
        # Arrange
        test_task = task()
        task_id = test_task.id
        new_status = TaskStatus.COMPLETED
        
        updated_task = Task(
            id=test_task.id,
            title=test_task.title,
            description=test_task.description,
            status=new_status,
            due_date=test_task.due_date,
            user_id=test_task.user_id,
            created_at=test_task.created_at,
            updated_at=datetime.now()
        )
        
        self.task_repository.get_by_id.return_value = test_task
        self.task_repository.update.return_value = updated_task
        
        # Act
        result = await self.service.update_task_status(
            task_id=task_id,
            status=new_status
        )
        
        # Assert
        assert result.status == new_status
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_task_status_not_found(self, faker):
        # Arrange
        task_id = faker.random_int()
        new_status = TaskStatus.COMPLETED
        
        self.task_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"No existe una tarea con el ID {task_id}"):
            await self.service.update_task_status(
                task_id=task_id,
                status=new_status
            )
        
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_task_successfully(self, task):
        # Arrange
        test_task = task()
        task_id = test_task.id
        
        self.task_repository.get_by_id.return_value = test_task
        self.task_repository.delete.return_value = True
        
        # Act
        result = await self.service.delete_task(task_id=task_id)
        
        # Assert
        assert result is True
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.delete.assert_awaited_once_with(task_id)

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, faker):
        # Arrange
        task_id = faker.random_int()
        
        self.task_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"No existe una tarea con el ID {task_id}"):
            await self.service.delete_task(task_id=task_id)
        
        self.task_repository.get_by_id.assert_awaited_once_with(task_id)
        self.task_repository.delete.assert_not_awaited() 