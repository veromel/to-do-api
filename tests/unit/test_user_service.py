import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime
import uuid

from src.application.services.user_service import UserService
from src.domain.models.user import User
from src.infrastructure.auth.jwt_auth_service import get_password_hash


@pytest.mark.unit
class TestUserService:
    def setup_method(self):
        self.user_repository = AsyncMock()
        self.service = UserService(user_repository=self.user_repository)

    @pytest.mark.asyncio
    async def test_create_user_successfully(self, faker, user):
        # Arrange
        new_user = user(
            id=1,
            username=faker.user_name(),
            email=faker.email(),
            hashed_password=get_password_hash(faker.password()),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.user_repository.get_by_email.return_value = None
        self.user_repository.get_by_username.return_value = None
        self.user_repository.create.return_value = new_user
        
        # Act
        result = await self.service.create_user(
            username=new_user.username,
            email=new_user.email,
            password=new_user.hashed_password
        )
        
        # Assert
        assert result.username == new_user.username
        assert result.email == new_user.email
        self.user_repository.get_by_email.assert_awaited_once_with(new_user.email)
        self.user_repository.get_by_username.assert_awaited_once_with(new_user.username)
        self.user_repository.create.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_user_with_existing_email_raises_error(self, faker, user):
        # Arrange
        existing_user = user()
        username = faker.user_name()
        email = existing_user.email
        password = faker.password()
        
        self.user_repository.get_by_email.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"Ya existe un usuario con el email {email}"):
            await self.service.create_user(
                username=username,
                email=email,
                password=password
            )
        
        self.user_repository.get_by_email.assert_awaited_once_with(email)
        self.user_repository.create.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_user_with_existing_username_raises_error(self, faker, user):
        # Arrange
        existing_user = user()
        username = existing_user.username
        email = faker.email()
        password = faker.password()
        
        self.user_repository.get_by_email.return_value = None
        self.user_repository.get_by_username.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"Ya existe un usuario con el username {username}"):
            await self.service.create_user(
                username=username,
                email=email,
                password=password
            )
        
        self.user_repository.get_by_email.assert_awaited_once_with(email)
        self.user_repository.get_by_username.assert_awaited_once_with(username)
        self.user_repository.create.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_authenticate_user_successfully(self, user, faker):
        # Arrange
        password = "test_password"
        hashed_password = get_password_hash(password)
        
        test_user = user()
        test_user.hashed_password = hashed_password
        
        self.user_repository.get_by_username.return_value = test_user
        
        # Act
        result = await self.service.authenticate_user(
            username=test_user.username,
            password=password
        )
        
        # Assert
        assert result is not None
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        self.user_repository.get_by_username.assert_awaited_once_with(test_user.username)

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_username(self, faker):
        # Arrange
        username = faker.user_name()
        password = faker.password()
        
        self.user_repository.get_by_username.return_value = None
        
        # Act
        result = await self.service.authenticate_user(
            username=username,
            password=password
        )
        
        # Assert
        assert result is None
        self.user_repository.get_by_username.assert_awaited_once_with(username)

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_password(self, user, faker):
        # Arrange
        correct_password = "correct_password"
        incorrect_password = "incorrect_password"
        hashed_password = get_password_hash(correct_password)
        
        test_user = user()
        test_user.hashed_password = hashed_password
        
        self.user_repository.get_by_username.return_value = test_user
        
        # Act
        result = await self.service.authenticate_user(
            username=test_user.username,
            password=incorrect_password
        )
        
        # Assert
        assert result is None
        self.user_repository.get_by_username.assert_awaited_once_with(test_user.username)

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user):
        # Arrange
        test_user = user()
        user_id = test_user.id
        
        self.user_repository.get_by_id.return_value = test_user
        
        # Act
        result = await self.service.get_user_by_id(user_id)
        
        # Assert
        assert result == test_user
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_username(self, user):
        # Arrange
        test_user = user()
        username = test_user.username
        
        self.user_repository.get_by_username.return_value = test_user
        
        # Act
        result = await self.service.get_user_by_username(username)
        
        # Assert
        assert result == test_user
        self.user_repository.get_by_username.assert_awaited_once_with(username)

    @pytest.mark.asyncio
    async def test_get_all_users(self, user):
        # Arrange
        users = [user() for _ in range(3)]
        skip = 0
        limit = 10
        
        self.user_repository.get_all.return_value = users
        
        # Act
        result = await self.service.get_all_users(skip, limit)
        
        # Assert
        assert result == users
        self.user_repository.get_all.assert_awaited_once_with(skip, limit)

    @pytest.mark.asyncio
    async def test_update_user_successfully(self, user, faker):
        # Arrange
        test_user = user()
        user_id = test_user.id
        new_username = faker.user_name()
        new_email = faker.email()
        new_password = faker.password()
        
        self.user_repository.get_by_id.return_value = test_user
        self.user_repository.get_by_username.return_value = None
        self.user_repository.get_by_email.return_value = None
        
        updated_user = User(
            id=test_user.id,
            username=new_username,
            email=new_email,
            hashed_password=get_password_hash(new_password),
            created_at=test_user.created_at,
            updated_at=datetime.now()
        )
        
        self.user_repository.update.return_value = updated_user
        
        # Act
        result = await self.service.update_user(
            user_id=user_id,
            username=new_username,
            email=new_email,
            password=new_password
        )
        
        # Assert
        assert result == updated_user
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)
        self.user_repository.get_by_username.assert_awaited_once_with(new_username)
        self.user_repository.get_by_email.assert_awaited_once_with(new_email)
        self.user_repository.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, faker):
        # Arrange
        user_id = faker.random_int()
        new_username = faker.user_name()
        
        self.user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"No existe un usuario con el ID {user_id}"):
            await self.service.update_user(user_id=user_id, username=new_username)
        
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)
        self.user_repository.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_user_username_already_exists(self, user, faker):
        # Arrange
        test_user = user()
        user_id = test_user.id
        
        existing_user = user()
        new_username = existing_user.username
        
        self.user_repository.get_by_id.return_value = test_user
        self.user_repository.get_by_username.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"Ya existe un usuario con el username {new_username}"):
            await self.service.update_user(user_id=user_id, username=new_username)
        
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)
        self.user_repository.get_by_username.assert_awaited_once_with(new_username)
        self.user_repository.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_user_successfully(self, user):
        # Arrange
        test_user = user()
        user_id = test_user.id
        
        self.user_repository.get_by_id.return_value = test_user
        self.user_repository.delete.return_value = True
        
        # Act
        result = await self.service.delete_user(user_id)
        
        # Assert
        assert result is True
        self.user_repository.get_by_id.assert_awaited_once_with(user_id)
        self.user_repository.delete.assert_awaited_once_with(user_id)