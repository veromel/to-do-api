from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import inject

from src.application.services.user_service import UserService
from apps.http.schemas import Token
from apps.http.docs import ApiDocs


auth_docs = ApiDocs.get_docs("auth_docs")

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/token", 
    response_model=Token, 
    **auth_docs.get("login_for_access_token", {})
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = inject.instance(UserService)

    try:
        token_data = await user_service.authenticate_user(
            username=form_data.username, 
            password=form_data.password
        )

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
