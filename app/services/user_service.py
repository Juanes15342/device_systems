from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate

def crear_usuario(db: Session, usuario: UserCreate):
    existente = db.query(User).filter(User.email == usuario.email).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )
    nuevo = User(**usuario.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_todos(db: Session, role: str = None, is_active: bool = None, order_by: str = "id"):
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if order_by == "name":
        query = query.order_by(User.name)
    elif order_by == "created_at":
        query = query.order_by(User.created_at)
    else:
        query = query.order_by(User.id)

    return query.all()

def obtener_por_id(db: Session, user_id: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="El ID debe ser un número positivo"
        )
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id {user_id} no encontrado"
        )
    return usuario

def obtener_por_email(db: Session, email: str):
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con email {email} no encontrado"
        )
    return usuario

def actualizar_usuario(db: Session, user_id: int, datos: UserCreate):
    usuario = obtener_por_id(db, user_id)

    duplicado = db.query(User).filter(
        User.email == datos.email,
        User.id != user_id
    ).first()
    if duplicado:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado por otro usuario"
        )

    for campo, valor in datos.model_dump().items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario

def actualizar_parcial(db: Session, user_id: int, datos: UserUpdate):
    campos = datos.model_dump(exclude_none=True)
    if not campos:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    usuario = obtener_por_id(db, user_id)

    if "email" in campos:
        duplicado = db.query(User).filter(
            User.email == campos["email"],
            User.id != user_id
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado por otro usuario"
            )

    for campo, valor in campos.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, user_id: int):
    usuario = obtener_por_id(db, user_id)
    db.delete(usuario)
    db.commit()
    return {"message": f"Usuario con id {user_id} eliminado correctamente"}