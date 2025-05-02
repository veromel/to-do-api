FROM python:3.10-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry==1.7.1

# Copiar archivos de configuración de dependencias
COPY pyproject.toml poetry.lock* /app/

# Configurar Poetry para que no cree un entorno virtual dentro del contenedor
RUN poetry config virtualenvs.create false

# Instalar dependencias
RUN poetry install --no-interaction --no-ansi

# Copiar el código de la aplicación
COPY . /app/

# Agregar el directorio actual al PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "apps.http.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"] 