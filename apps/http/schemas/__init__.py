"""
Módulo de esquemas HTTP para la API.
Reexporta los esquemas desde sus módulos respectivos para facilitar las importaciones.
"""

# Exportar esquemas de usuarios
from apps.http.schemas.users_http_schema import (
    UserBase,
    UserCreate,
    UserUpdate,
    User,
    UserList,
    Token,
    TokenData,
)

# Exportar esquemas de tareas
from apps.http.schemas.tasks_http_schema import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    Task,
    TaskList,
)
