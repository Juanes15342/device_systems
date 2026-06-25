from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
from typing import Optional
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Mínimo 3 caracteres")
    email: EmailStr
    role: RoleEnum
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío o ser solo espacios")
        return v.strip()

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None