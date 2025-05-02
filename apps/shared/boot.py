import logging
import inject

from apps.shared.dependencies import Dependencies
from src.infrastructure.database import SessionLocal
from src.infrastructure.config import get_settings

# Obtener configuración
settings = get_settings()

# Configurar logging
logger = logging.getLogger("todo-api")


class Boot:
    """
    Inicializa la aplicación, configurando las dependencias y la conexión a la base de datos.
    """

    def __init__(self):
        logger.info("Iniciando la configuración de la aplicación...")
        self.settings = settings
        self._configure_dependencies()
        logger.info("Configuración de la aplicación completada.")

    def _configure_dependencies(self):
        """Configura la inyección de dependencias con inject."""
        if inject.is_configured():
            logger.info("La inyección de dependencias ya está configurada.")
            return

        try:
            db_session = SessionLocal()

            def config(binder):
                dependencies = Dependencies.app(db_session)

                for interface, implementation in dependencies:
                    binder.bind(interface, implementation)

                logger.info(f"Registradas {len(dependencies) + 2} dependencias.")

            inject.configure(config)

        except Exception as e:
            logger.critical(
                f"Error al configurar dependencias: {str(e)}", exc_info=True
            )
            raise SystemExit(f"No se pudo iniciar la aplicación: {str(e)}")


boot = Boot()
