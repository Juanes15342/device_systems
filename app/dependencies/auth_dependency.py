from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.auth.security import decode_access_token
from app.models.user_model import User

# Indica a Swagger dónde está el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Valida el token JWT y retorna el usuario correspondiente."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    usuario = db.query(User).filter(User.email == email).first()
    if usuario is None:
        raise credentials_exception

    return usuario


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario autenticado esté activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Permite acceso solo a administradores."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return current_user


def require_admin_or_support(current_user: User = Depends(get_current_active_user)) -> User:
    """Permite acceso a administradores o soporte."""
    if current_user.role not in ("admin", "support"):
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador o soporte")
    return current_user