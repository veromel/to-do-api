from datetime import datetime
import inject
from fastapi import APIRouter, HTTPException, status, Query, Path, Depends
from typing import List

from src.application.services.task_service import TaskService
from src.domain.models.user import User as UserEntity
from src.domain.models.task import TaskStatus
from apps.http.schemas import TaskCreate, Task, TaskList, TaskUpdate, TaskStatusUpdate
from apps.http.auth_middleware import get_current_user
from apps.http.docs import ApiDocs

task_docs = ApiDocs.get_docs("tasks_docs")

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post(
    "/", 
    response_model=Task, 
    status_code=status.HTTP_201_CREATED, 
    **task_docs.get("create_task", {})
)
async def create_task(
        task_data: TaskCreate,
        current_user: UserEntity = Depends(get_current_user)
):
    try:
        task_service = inject.instance(TaskService)

        task = await task_service.create_task(
            user_id=current_user.id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            due_date=task_data.due_date
        )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@tasks_router.get(
    "/", 
    response_model=TaskList, 
    **task_docs.get("get_tasks", {})
)
async def get_tasks(
        status: TaskStatus = Query(None, description="Filtrar por estado (PENDING, IN_PROGRESS, COMPLETED)"),
        due_date_from: datetime = Query(None, description="Filtrar por fecha de vencimiento desde (formato ISO)"),
        due_date_to: datetime = Query(None, description="Filtrar por fecha de vencimiento hasta (formato ISO)"),
        skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
        limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a devolver (paginación)"),
        current_user: UserEntity = Depends(get_current_user)
):
    try:
        task_service = inject.instance(TaskService)

        tasks = await task_service.get_user_tasks(
            user_id=current_user.id,
            status=status,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            skip=skip,
            limit=limit
        )

        return {
            "total": len(tasks),
            "items": tasks
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@tasks_router.get(
    "/{task_id}", 
    response_model=Task, 
    **task_docs.get("get_task", {})
)
async def get_task(
        task_id: int = Path(..., ge=1, description="ID de la tarea"),
        current_user: UserEntity = Depends(get_current_user)
):
    return await _get_user_task_or_404(task_id, current_user)


@tasks_router.patch(
    "/{task_id}", 
    response_model=Task, 
    **task_docs.get("update_task", {})
)
async def update_task(
        task_data: TaskUpdate,
        task_id: int = Path(..., ge=1, description="ID de la tarea"),
        current_user: UserEntity = Depends(get_current_user)
):
    await _get_user_task_or_404(task_id, current_user)
    
    try:
        update_data = {}
        if task_data.title is not None:
            update_data['title'] = task_data.title
        if task_data.description is not None:
            update_data['description'] = task_data.description
        if task_data.status is not None:
            update_data['status'] = task_data.status
        if task_data.due_date is not None:
            update_data['due_date'] = task_data.due_date

        task_service = inject.instance(TaskService)
        updated_task = await task_service.update_task(task_id=task_id, **update_data)

        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@tasks_router.patch(
    "/{task_id}/status", 
    response_model=Task, 
    **task_docs.get("update_task_status", {})
)
async def update_task_status(
        status_data: TaskStatusUpdate,
        task_id: int = Path(..., ge=1, description="ID de la tarea"),
        current_user: UserEntity = Depends(get_current_user)
):
    await _get_user_task_or_404(task_id, current_user)
    
    try:
        task_service = inject.instance(TaskService)
        updated_task = await task_service.update_task(task_id=task_id, status=status_data.status)

        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@tasks_router.delete(
    "/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    **task_docs.get("delete_task", {})
)
async def delete_task(
        task_id: int = Path(..., ge=1, description="ID de la tarea"),
        current_user: UserEntity = Depends(get_current_user)
):
    await _get_user_task_or_404(task_id, current_user)
    
    try:
        task_service = inject.instance(TaskService)
        result = await task_service.delete_task(task_id=task_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la tarea"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def _get_user_task_or_404(task_id: int, current_user: UserEntity) -> Task:
    task_service = inject.instance(TaskService)
    task = await task_service.get_task_by_id(task_id=task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    return task
