from fastapi import APIRouter, HTTPException, Query, Response
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum
from typing import Optional

router = APIRouter()

# Base de datos simulada en memoria
usuarios_db: list[dict] = [
    {"id": 1, "name": "Carlos Admin", "email": "carlos@mail.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Laura Support", "email": "laura@mail.com", "role": "support", "is_active": True},
    {"id": 3, "name": "Pedro User", "email": "pedro@mail.com", "role": "user", "is_active": False},
]

def agregar_cabeceras(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# GET /users — listar todos, con filtros opcionales
@router.get("/users", response_model=list[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum] = Query(default=None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(default=None, description="Filtrar por estado activo")
):
    agregar_cabeceras(response)
    resultado = usuarios_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


# GET /users/{user_id} — buscar por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int, response: Response):
    agregar_cabeceras(response)
    for usuario in usuarios_db:
        if usuario["id"] == user_id:
            return usuario
    raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")


# POST /users — crear nuevo usuario
@router.post("/users", response_model=UserResponse, status_code=201)
def crear_usuario(usuario: UserCreate, response: Response):
    agregar_cabeceras(response)

    # Verificar email duplicado
    for u in usuarios_db:
        if u["email"] == usuario.email:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_id = max(u["id"] for u in usuarios_db) + 1
    nuevo_usuario = {"id": nuevo_id, **usuario.model_dump()}
    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario