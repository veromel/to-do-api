from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(
        ..., description="Nombre de usuario", min_length=3, max_length=50
    )
    email: EmailStr = Field(..., description="Correo electrónico")


class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña", min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, description="Nombre de usuario", min_length=3, max_length=50
    )
    email: Optional[EmailStr] = Field(None, description="Correo electrónico")
    password: Optional[str] = Field(None, description="Contraseña", min_length=6)


class User(UserBase):
    id: int = Field(..., description="ID del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class UserList(BaseModel):
    total: int = Field(..., description="Número total de usuarios")
    items: List[User] = Field(..., description="Lista de usuarios")


class Token(BaseModel):
    access_token: str = Field(..., description="Token de acceso")
    token_type: str = Field(..., description="Tipo de token")


class TokenData(BaseModel):
    username: Optional[str] = None
