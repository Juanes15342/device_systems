from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token


def registrar_usuario(db: Session, datos: UserRegister):
    existente = db.query(User).filter(User.email == datos.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = User(
        name=datos.name,
        email=datos.email,
        hashed_password=get_password_hash(datos.password),
        role=datos.role,
        is_active=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def autenticar_usuario(db: Session, email: str, password: str):
    usuario = db.query(User).filter(User.email == email).first()

    if not usuario or not verify_password(password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not usuario.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    access_token = create_access_token(
        data={"sub": usuario.email, "role": usuario.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}