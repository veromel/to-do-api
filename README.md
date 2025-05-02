# API de Gestión de Tareas (To-Do API)

API REST para gestionar una lista de tareas por usuario implementada con FastAPI, SQLAlchemy y arquitectura hexagonal.

## Repositorio

[GitHub: https://github.com/veromel/to-do-api](https://github.com/veromel/to-do-api)

## Índice
1. [✨ Características](#características)
2. [🏗️ Arquitectura](#arquitectura)
3. [🛠️ Tecnologías utilizadas](#tecnologías-utilizadas)
4. [📋 Requisitos](#requisitos)
5. [🚀 Instalación y ejecución](#instalación-y-ejecución)
6. [⚙️ Configuración](#configuración)
7. [📚 Documentación de la API](#documentación-de-la-api)
8. [🔌 Endpoints](#endpoints)
9. [🧪 Uso con Postman](#uso-con-postman)
10. [🧪 Ejecución de Tests](#ejecución-de-tests)
11. [🧠 Decisiones técnicas](#decisiones-técnicas)
12. [🚧 Dificultades encontradas](#dificultades-encontradas)

## ✨ Características

- Registro y gestión de usuarios
- CRUD completo de tareas asociadas a usuarios
- Autenticación mediante tokens JWT
- Filtros para búsqueda de tareas (por estado, fecha, etc.)
- Paginación implementada
- Documentación automática con Swagger UI
- Tests unitarios para los servicios principales

## 🏗️ Arquitectura

El proyecto está estructurado siguiendo los principios de una **arquitectura hexagonal** (también conocida como Ports and Adapters), que permite separar la lógica de negocio de los detalles de implementación. 

La estructura principal es:

```
to_do_api/
│
├── src/                          # Código fuente principal
│   ├── domain/                   # Modelos de dominio y puertos (interfaces)
│   │   ├── models/               # Entidades de dominio (User, Task)
│   │   └── ports/                # Interfaces de repositorios
│   │
│   ├── application/              # Lógica de aplicación
│   │   └── services/             # Servicios que implementan los casos de uso
│   │
│   └── infrastructure/           # Implementaciones concretas
│       ├── auth/                 # Servicio de autenticación JWT
│       ├── repositories/         # Implementaciones de los repositorios
│       ├── schemas/              # Esquemas ORM para SQLAlchemy
│       ├── config.py             # Configuración de la aplicación
│       └── database.py           # Configuración y conexión a la base de datos
│
├── apps/                         # Aplicaciones (adaptadores)
│   ├── http/                     # API REST con FastAPI
│   │   ├── docs/                 # Documentación JSON para Swagger
│   │   ├── routers/              # Endpoints de la API
│   │   ├── schemas/              # Esquemas de request/response (Pydantic)
│   │   ├── auth_middleware.py    # Middleware de autenticación
│   │   └── main.py               # Punto de entrada de la aplicación FastAPI
│   │
│   └── shared/                   # Componentes compartidos
│       └── boot.py               # Configuración de inyección de dependencias
│
├── tests/                        # Tests unitarios
│
├── Dockerfile                    # Configuración para Docker
├── docker-compose.yml           # Configuración para Docker Compose
├── pyproject.toml                # Configuración de Poetry y dependencias
└── poetry.lock                   # Bloqueo de versiones de dependencias
```

## 🛠️ Tecnologías utilizadas

- **FastAPI**: Framework web de alto rendimiento
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **SQLite**: Base de datos relacional ligera
- **Poetry**: Gestión de dependencias y entorno virtual
- **Pydantic**: Validación de datos y serialización
- **Python-jose**: Implementación de JWT para autenticación
- **Inject**: Inyección de dependencias
- **Docker**: Contenedorización de la aplicación
- **Pytest**: Framework de testing

## 📋 Requisitos

Para ejecutar este proyecto necesitas tener instalado:

- Docker
- Docker Compose

## 🚀 Instalación y ejecución

La aplicación está configurada para ejecutarse mediante Docker, lo que garantiza un entorno consistente y evita problemas de dependencias o configuración.

1. Clona el repositorio:

```bash
git clone https://github.com/veromel/to-do-api.git
cd to_do_api
```

2. Construye y ejecuta los contenedores:

```bash
docker-compose up --build
```

Para ejecutar en segundo plano:

```bash
docker-compose up -d
```

Para detener los contenedores:

```bash
docker-compose down
```

Una vez en ejecución, la API estará disponible en http://localhost:8000

## ⚙️ Configuración

La aplicación utiliza un sistema flexible de configuración que permite definir los parámetros de tres maneras diferentes (en orden de prioridad):

1. **Variables de entorno del sistema** con el prefijo `TODO_`
2. **Archivo `.env`** en la raíz del proyecto 
3. **Valores predeterminados** en el código

La configuración se define en el archivo `docker-compose.yml` para el entorno Docker, pero también puedes modificar el archivo `.env` o establecer variables de entorno directamente en tu sistema.

```env
# Ejemplo de archivo .env o variables de entorno con prefijo TODO_
TODO_DATABASE_URL=sqlite+aiosqlite:///./todo_api.db
TODO_SECRET_KEY=supersecretkey
TODO_ALGORITHM=HS256
TODO_ACCESS_TOKEN_EXPIRE_MINUTES=30
TODO_DEBUG=True
TODO_API_V1_STR=/api
```

### Variables de configuración disponibles

| Variable | Descripción | Valor por defecto |
|----------|-------------|------------------|
| `TODO_DATABASE_URL` | URL de conexión a la base de datos | `sqlite+aiosqlite:///./todo_api.db` |
| `TODO_SECRET_KEY` | Clave secreta para JWT | `supersecretkey` |
| `TODO_ALGORITHM` | Algoritmo de cifrado para JWT | `HS256` |
| `TODO_ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token JWT | `30` |
| `TODO_DEBUG` | Modo de depuración | `False` |
| `TODO_API_V1_STR` | Prefijo para los endpoints de la API | `/api` |

Para el entorno de desarrollo o prueba, los valores predeterminados son suficientes.

## 📚 Documentación de la API

La documentación interactiva de la API se genera automáticamente y está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Autenticación

- `POST /api/auth/token` - Obtener token JWT
  - Requiere: username y password en form-data
  - Retorna: access_token y token_type

### Usuarios

- `POST /api/users/` - Crear usuario
  - Requiere: username, email, password
  - No requiere autenticación

- `GET /api/users/` - Listar usuarios
  - Parámetros opcionales: skip, limit
  - Requiere autenticación

- `GET /api/users/{id}/` - Obtener usuario por ID
  - Requiere autenticación

- `PATCH /api/users/{id}/` - Actualizar usuario
  - Requiere autenticación
  - Solo el propio usuario o admin puede actualizar

- `DELETE /api/users/{id}/` - Eliminar usuario
  - Requiere autenticación
  - Solo el propio usuario o admin puede eliminar

### Tareas

- `POST /api/tasks/` - Crear tarea
  - Requiere: title, description (opcional), due_date (opcional), status
  - Requiere autenticación

- `GET /api/tasks/` - Listar tareas
  - Parámetros opcionales: status, due_date_start, due_date_end, skip, limit
  - Requiere autenticación
  - Filtra por tareas del usuario autenticado

- `GET /api/tasks/{id}/` - Obtener detalle de una tarea
  - Requiere autenticación
  - Solo el propietario puede ver sus tareas

- `PATCH /api/tasks/{id}/` - Actualizar tarea
  - Requiere autenticación
  - Solo el propietario puede actualizar

- `PATCH /api/tasks/{id}/status` - Actualizar estado de tarea
  - Requiere: status
  - Requiere autenticación
  - Solo el propietario puede actualizar

- `DELETE /api/tasks/{id}/` - Eliminar tarea
  - Requiere autenticación
  - Solo el propietario puede eliminar

## 🧪 Uso con Postman

1. **Crear un usuario**:
   - Método: POST
   - URL: http://localhost:8000/api/users/
   - Body (JSON):
     ```json
     {
       "username": "usuario1",
       "email": "usuario1@example.com",
       "password": "contraseña123"
     }
     ```

2. **Obtener token JWT**:
   - Método: POST
   - URL: http://localhost:8000/api/auth/token
   - Body (form-data):
     - username: usuario1
     - password: contraseña123

3. **Utilizar el token para autenticación**:
   - En todas las peticiones posteriores, añadir el header:
     - Authorization: Bearer [token obtenido]

4. **Crear una tarea**:
   - Método: POST
   - URL: http://localhost:8000/api/tasks/
   - Headers: Authorization: Bearer [token]
   - Body (JSON):
     ```json
     {
       "title": "Mi primera tarea",
       "description": "Descripción de la tarea",
       "status": "pendiente",
       "due_date": "2023-12-31T23:59:59Z"
     }
     ```

5. **Obtener todas las tareas**:
   - Método: GET
   - URL: http://localhost:8000/api/tasks/
   - Headers: Authorization: Bearer [token]

6. **Filtrar tareas**:
   - Método: GET
   - URL: http://localhost:8000/api/tasks/?status=pendiente&limit=10&skip=0
   - Headers: Authorization: Bearer [token]

La colección de Postman completa está disponible en el archivo `postman_collection.json`.

## 🧪 Ejecución de Tests

El proyecto incluye pruebas unitarias utilizando pytest para verificar la correcta implementación de los servicios principales.

### Cómo ejecutar las pruebas

Las pruebas se pueden ejecutar utilizando pytest:

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con información detallada
pytest -v

# Ejecutar una prueba específica
pytest tests/unit/test_task_service.py
```

### Estructura de tests

Las pruebas están organizadas principalmente en:

- Tests unitarios para servicios de usuario (`test_user_service.py`)
- Tests unitarios para servicios de tareas (`test_task_service.py`)

Estas pruebas validan:
- Creación, actualización y eliminación de usuarios y tareas
- Manejo de errores para casos excepcionales
- Autenticación de usuarios
- Filtrado y búsqueda de tareas

Los tests utilizan mocks para simular las dependencias y se centran en probar la lógica de negocio de forma aislada.

## 🧠 Decisiones técnicas

### Arquitectura Hexagonal

Se implementó una arquitectura hexagonal para desacoplar la lógica de negocio de los detalles de implementación (base de datos, API, etc.). Esto permite:

- **Mayor testabilidad**: Los componentes pueden probarse de forma aislada.
- **Flexibilidad**: Facilita el cambio de implementaciones sin modificar la lógica de negocio.
- **Separación de responsabilidades**: Cada capa tiene una responsabilidad bien definida.


### Inyección de Dependencias

Se utilizó el patrón de inversión de dependencias con la librería `inject` para:

- Desacoplar componentes de sus implementaciones concretas
- Facilitar la prueba unitaria mediante mocks
- Permitir el intercambio de implementaciones sin modificar el código del dominio

### ORM y Base de Datos

- **SQLAlchemy**: Se eligió como ORM para abstraer el acceso a la base de datos, evitando inyectar SQL directo.
- **SQLite**: Como motor de base de datos por su simplicidad.

### Autenticación y Seguridad

- **JWT**: Se implementó autenticación basada en tokens JWT utilizando la librería `python-jose`.
- **Hashing de contraseñas**: Se utiliza `passlib` con bcrypt para el almacenamiento seguro de contraseñas.

### Contenedorización

- **Docker**: Se utilizó para garantizar la consistencia entre entornos de desarrollo y facilitar el despliegue.

### Documentación

- **Swagger UI y ReDoc**: Generados automáticamente por FastAPI.
- **Esquemas JSON**: Se añadieron archivos JSON específicos para mejorar la documentación en Swagger.

### Testing

- **Pytest**: Se implementaron tests unitarios para los servicios de usuario y tareas.
- **Mocks**: Se utilizan mocks para simular las dependencias y aislar las unidades de código en los tests.

## 🚧 Dificultades encontradas

### Gestión de Dependencias Circulares

- **Problema**: Aparecieron dependencias circulares al implementar la inyección de dependencias.
- **Solución**: Se reorganizó la estructura del proyecto y se implementó un patrón de registro centralizado con el componente `Boot` para inicializar todas las dependencias al inicio de la aplicación.

### Operaciones Asíncronas

- **Problema**: Coordinar operaciones asíncronas con SQLAlchemy y FastAPI.
- **Solución**: Se implementó un patrón consistente para el manejo de operaciones asíncronas y se agregó soporte para SQLite asíncrono con `aiosqlite`.

### Implementación de Filtros

- **Problema**: Diseñar un sistema de filtrado flexible para las tareas.
- **Solución**: Se implementó un sistema que permite filtrar por múltiples criterios (estado, fecha, etc.) de forma opcional y componible utilizando kwargs, lo que facilita la extensión con nuevos filtros sin modificar la interfaz. 