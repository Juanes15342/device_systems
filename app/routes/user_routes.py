from fastapi import APIRouter, Query, Response, Depends
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum
from app.services import user_service
from app.dependencies.user_dependencies import agregar_cabeceras
from typing import Optional

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
):
    agregar_cabeceras(response)
    return user_service.obtener_todos(role=role, is_active=is_active)

@router.get("/users/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int, response: Response):
    agregar_cabeceras(response)
    return user_service.obtener_por_id(user_id)

@router.post("/users", response_model=UserResponse, status_code=201)
def crear_usuario(usuario: UserCreate, response: Response):
    agregar_cabeceras(response)
    return user_service.crear_usuario(usuario)