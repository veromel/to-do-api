from src.domain.ports.auth_service import AuthService
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.task_repository import TaskRepository
from src.infrastructure.auth.jwt_auth_service import JWTAuthService

from src.infrastructure.repositories.user_sql_repository import SQLAlchemyUserRepository
from src.infrastructure.repositories.task_sql_repository import SQLAlchemyTaskRepository

from src.infrastructure.database import SessionLocal


class Dependencies:
    @staticmethod
    def app(db_session=None):
        # Si no se proporciona una sesiónse crea una nueva
        if db_session is None:
            db_session = SessionLocal()

        # Repositorios
        user_repository = SQLAlchemyUserRepository(db_session)
        task_repository = SQLAlchemyTaskRepository(db_session)

        # Servicios
        auth_service = JWTAuthService()

        return [
            (UserRepository, user_repository),
            (TaskRepository, task_repository),
            (AuthService, auth_service),
        ]
