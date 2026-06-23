from fastapi import APIRouter, Query, Response, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, RoleEnum
from app.services import user_service
from app.dependencies.database_dependency import agregar_cabeceras
from app.dependencies.database_dependency import get_db
from typing import Optional
from app.schemas.loan_schema import LoanResponse
from app.services import loan_service

router = APIRouter()

@router.get("/users/{user_id}/loans", response_model=list[LoanResponse], status_code=200)
def loans_de_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return loan_service.obtener_loans_por_usuario(db, user_id)

@router.get(
    "/users",
    response_model=list[UserResponse],
    status_code=200,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por rol y estado, y ordenar resultados."
)
def listar_usuarios(
    response: Response,
    db: Session = Depends(get_db),
    role: Optional[RoleEnum] = Query(default=None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(default=None, description="Filtrar por estado: true o false"),
    order_by: Optional[str] = Query(default="id", description="Ordenar por: id, name, created_at")
):
    agregar_cabeceras(response)
    return user_service.obtener_todos(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico. Responde 404 si no existe.",
    responses={404: {"description": "Usuario no encontrado"}}
)
def obtener_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return user_service.obtener_por_id(db, user_id)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario. El email debe ser único. Valida todos los campos con Pydantic.",
    responses={
        201: {"description": "Usuario creado correctamente"},
        400: {"description": "Email duplicado"},
        422: {"description": "Error de validación"}
    }
)
def crear_usuario(usuario: UserCreate, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return user_service.crear_usuario(db, usuario)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Actualizar usuario completo",
    description="Reemplaza completamente los datos de un usuario. Todos los campos son obligatorios.",
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Email duplicado"}
    }
)
def actualizar_usuario(
    user_id: int,
    usuario: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario(db, user_id, usuario)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Actualizar usuario parcialmente",
    description="Modifica solo los campos enviados. Mínimo un campo requerido.",
    responses={
        400: {"description": "Sin campos para actualizar o email duplicado"},
        404: {"description": "Usuario no encontrado"}
    }
)
def actualizar_parcial(
    user_id: int,
    datos: UserUpdate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_parcial(db, user_id, datos)


@router.delete(
    "/users/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario por ID. Responde 204 sin cuerpo si fue exitoso.",
    responses={
        204: {"description": "Usuario eliminado correctamente"},
        404: {"description": "Usuario no encontrado"}
    }
)
def eliminar_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    user_service.eliminar_usuario(db, user_id)