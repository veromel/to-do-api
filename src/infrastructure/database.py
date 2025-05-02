from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import logging

from src.infrastructure.config import get_settings

logger = logging.getLogger("todo-api")

settings = get_settings()

# Crear motor de base de datos asíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    ),
    echo=settings.DB_ECHO,  # Usar configuración para habilitar/deshabilitar logs SQL
)

# Configurar sesión
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Base para modelos declarativos
Base = declarative_base()


async def init_db():
    logger.info("Inicializando la base de datos...")
    async with engine.begin() as conn:
        # Crear tablas si no existen
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Base de datos inicializada correctamente.")
