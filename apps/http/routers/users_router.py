import inject
from fastapi import APIRouter, HTTPException, status, Query, Path, Depends

from src.application.services.user_service import UserService
from src.domain.models.user import User as UserEntity
from apps.http.schemas import UserCreate, User, UserList, UserUpdate
from apps.http.auth_middleware import get_current_user
from apps.http.docs import ApiDocs


users_docs = ApiDocs.get_docs("users_docs")

users_router = APIRouter(prefix="/users")


@users_router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    **users_docs.get("create_user", {})
)
async def create_user(user_data: UserCreate):
    try:
        user_service = inject.instance(UserService)
        user = await user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@users_router.get(
    "/me", 
    response_model=User, 
    **users_docs.get("get_current_user_info", {})
)
async def get_current_user_info(current_user: UserEntity = Depends(get_current_user)):
    return current_user


@users_router.get(
    "/", 
    response_model=UserList, 
    **users_docs.get("get_users", {})
)
async def get_users(
        skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
        limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a devolver (paginación)"),
        current_user: UserEntity = Depends(get_current_user)
):
    user_service = inject.instance(UserService)
    users = await user_service.get_all_users(skip=skip, limit=limit)

    return {
        "total": len(users),
        "items": users
    }


@users_router.get(
    "/{user_id}", 
    response_model=User, 
    **users_docs.get("get_user", {})
)
async def get_user(
        user_id: int = Path(..., ge=1, description="ID del usuario"),
        current_user: UserEntity = Depends(get_current_user)
):
    user_service = inject.instance(UserService)
    user = await user_service.get_user_by_id(user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    return user


@users_router.patch(
    "/me", 
    response_model=User, 
    **users_docs.get("update_current_user", {})
)
async def update_current_user(
        user_data: UserUpdate, 
        current_user: UserEntity = Depends(get_current_user)
):
    try:
        updates = {}
        if user_data.username is not None:
            updates["username"] = user_data.username
        if user_data.email is not None:
            updates["email"] = user_data.email
        if user_data.password is not None:
            updates["password"] = user_data.password

        user_service = inject.instance(UserService)
        updated_user = await user_service.update_user(
            user_id=current_user.id,
            **updates
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@users_router.delete(
    "/me", 
    status_code=status.HTTP_204_NO_CONTENT, 
    **users_docs.get("delete_current_user", {})
)
async def delete_current_user(current_user: UserEntity = Depends(get_current_user)):
    try:
        user_service = inject.instance(UserService)
        result = await user_service.delete_user(user_id=current_user.id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error al eliminar el usuario"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
