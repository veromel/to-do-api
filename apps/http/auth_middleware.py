import inject
import traceback
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from src.domain.ports.auth_service import AuthService
from src.application.services.user_service import UserService

# Configurar el endpoint de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """
    Dependencia para obtener el ID del usuario desde un token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Obtener servicio de autenticación mediante inject
        auth_service = inject.instance(AuthService)

        # Validar token
        payload = auth_service.validate_token(token)
        if not payload:
            raise credentials_exception

        # Obtener el ID del usuario del token
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception

        return user_id
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"Error al obtener el user_id del token: {str(e)}")
        print(traceback.format_exc())
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtener el usuario actual autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Obtener servicio de autenticación y usuario
        auth_service = inject.instance(AuthService)
        user_service = inject.instance(UserService)

        # Validar token
        payload = auth_service.validate_token(token)
        if not payload:
            raise credentials_exception

        # Obtener el username del token
        username = payload.get("sub")
        if not username:
            raise credentials_exception

        # Obtener usuario por username
        user = await user_service.get_user_by_username(username)
        if not user:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"Error al obtener el usuario actual: {str(e)}")
        print(traceback.format_exc())
        raise credentials_exception
