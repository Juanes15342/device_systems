from app.data.users_db import usuarios_db
from app.schemas.user_schema import UserCreate
from fastapi import HTTPException

def obtener_todos(role=None, is_active=None):
    resultado = usuarios_db
    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]
    return resultado

def obtener_por_id(user_id: int):
    for usuario in usuarios_db:
        if usuario["id"] == user_id:
            return usuario
    raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")

def crear_usuario(usuario: UserCreate):
    for u in usuarios_db:
        if u["email"] == usuario.email:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
    nuevo_id = max(u["id"] for u in usuarios_db) + 1
    nuevo_usuario = {"id": nuevo_id, **usuario.model_dump()}
    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario