import uvicorn
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware import Middleware

from apps.http.routers import router
from apps.shared.boot import Boot
from src.infrastructure.database import init_db
from src.infrastructure.config import get_settings

# Importar todos los modelos para que SQLAlchemy los reconozca
from src.infrastructure.schemas.user_schema import UserSchema
from src.infrastructure.schemas.task_schema import TaskSchema

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todo-api")

# Obtener configuración
settings = get_settings()


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_middleware() -> list[Middleware]:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador de eventos de ciclo de vida de la aplicación.
    Se ejecuta al inicio y al cierre de la aplicación.
    """
    # Código que se ejecuta antes de que la aplicación comience a recibir tráfico
    logger.info("Inicializando la aplicación...")
    
    # Iniciar Boot para configurar inyección de dependencias
    logger.info("Inicializando Boot...")
    Boot()
    logger.info("Boot inicializado correctamente.")
    
    # Inicializar la base de datos
    await init_db()
    logger.info("Aplicación iniciada correctamente.")
    
    yield  # La aplicación se ejecuta aquí
    
    # Código que se ejecuta cuando la aplicación se cierra
    logger.info("Aplicación detenida.")


def create_app() -> FastAPI:
    app = FastAPI(
        title="API de Gestión de Tareas",
        description="""
        # API de Gestión de Tareas
        
        Esta API permite gestionar tareas y usuarios en una aplicación de To-Do.
        
        ## Funcionalidades
        
        * **Usuarios**: Crear, actualizar, eliminar y consultar usuarios
        * **Tareas**: Gestionar tareas por usuario (crear, modificar, actualizar estado, eliminar...)
        * **Autenticación**: Sistema de autenticación JWT
        
        ## Notas de uso
        
        Para usar esta API necesitas autenticarte primero con el endpoint `/api/auth/token`.
        Una vez autenticado, debes incluir el token JWT en el header `Authorization` con el formato `Bearer {token}`.
        """,
        version="1.0.0",
        middleware=init_middleware(),
        lifespan=lifespan,
    )
    
    # Inicializar los routers
    logger.info("Inicializando routers...")
    init_routers(app_=app)
    logger.info("Routers inicializados correctamente.")

    return app


if __name__ == "__main__":
    # Iniciar el servidor
    uvicorn.run(
        "apps.http.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )
