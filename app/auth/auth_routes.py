from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import UserRegister, Token, UserAuthResponse
from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.middlewares.rate_limiter import limiter

router = APIRouter()


@router.post(
    "/auth/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario con contraseña encriptada. Límite: 3 solicitudes por minuto.",
    responses={400: {"description": "Email ya registrado"}, 429: {"description": "Demasiadas solicitudes"}}
)
@limiter.limit("3/minute")
def register(request: Request, datos: UserRegister, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, datos)


@router.post(
    "/auth/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario y retorna un token JWT. Límite: 5 solicitudes por minuto.",
    responses={401: {"description": "Credenciales inválidas"}, 429: {"description": "Demasiadas solicitudes"}}
)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.autenticar_usuario(db, email=form_data.username, password=form_data.password)


@router.get(
    "/auth/me",
    response_model=UserAuthResponse,
    summary="Usuario autenticado actual",
    description="Retorna los datos del usuario propietario del token enviado."
)
def me(current_user: User = Depends(get_current_user)):
    return current_user