from fastapi import APIRouter, Query, Response, Depends
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusEnum
from app.services import loan_service
from app.dependencies.user_dependencies import agregar_cabeceras
from app.dependencies.database_dependency import get_db
from typing import Optional
from app.schemas.loan_schema import LoanDetailResponse
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from fastapi import APIRouter, Query, Response, Depends, Request
from app.middlewares.rate_limiter import limiter

router = APIRouter()

@router.get("/loans", response_model=list[LoanResponse], status_code=200)
def listar_loans(
    response: Response,
    db: Session = Depends(get_db),
    status: Optional[LoanStatusEnum] = Query(default=None)
):
    agregar_cabeceras(response)
    return loan_service.obtener_todos(db, status=status)

@router.get("/loans/{loan_id}", response_model=LoanResponse, status_code=200)
def obtener_loan(loan_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return loan_service.obtener_por_id(db, loan_id)

@router.post(
    "/loans",
    response_model=LoanResponse,
    status_code=201,
    summary="Crear un préstamo",
    description="Registra un nuevo préstamo. Límite: 10 solicitudes por minuto."
)
@limiter.limit("10/minute")
def crear_loan(
    request: Request,
    loan: LoanCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    agregar_cabeceras(response)
    return loan_service.crear_loan(db, loan)

@router.patch("/loans/{loan_id}/return", response_model=LoanResponse, status_code=200)
def devolver_loan(
    loan_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    agregar_cabeceras(response)
    return loan_service.devolver_loan(db, loan_id)

@router.get("/loans/details", response_model=list[LoanDetailResponse], status_code=200)
def detalles_loans(
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support),
    status: Optional[LoanStatusEnum] = Query(default=None),
    user_email: Optional[str] = Query(default=None),
    device_type: Optional[str] = Query(default=None)
):
    agregar_cabeceras(response)
    return loan_service.obtener_detalles(db, status=status, user_email=user_email, device_type=device_type)