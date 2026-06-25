from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    role: str = Field(default="user", description="admin, support o user")

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios en blanco")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v

    @field_validator("role")
    @classmethod
    def validar_role(cls, v: str) -> str:
        roles_permitidos = {"admin", "support", "user"}
        if v not in roles_permitidos:
            raise ValueError(f"Rol no permitido. Debe ser uno de: {roles_permitidos}")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class UserAuthResponse(BaseModel):
    """Respuesta segura tras registro/login — nunca incluye la contraseña."""
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)