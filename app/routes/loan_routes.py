from fastapi import APIRouter, Query, Response, Depends
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusEnum
from app.services import loan_service
from app.dependencies.user_dependencies import agregar_cabeceras
from app.dependencies.database_dependency import get_db
from typing import Optional
from app.schemas.loan_schema import LoanDetailResponse

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
    description="Registra un nuevo préstamo. Valida que el usuario y el dispositivo existan, "
                "y que el dispositivo esté disponible. Marca el dispositivo como no disponible.",
    response_description="Préstamo creado correctamente",
    responses={
        404: {"description": "Usuario o dispositivo no encontrado"},
        409: {"description": "El dispositivo no está disponible"},
        422: {"description": "Error de validación"}
    }
)
def crear_loan(loan: LoanCreate, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return loan_service.crear_loan(db, loan)


@router.patch(
    "/loans/{loan_id}/return",
    response_model=LoanResponse,
    status_code=200,
    summary="Devolver un préstamo",
    description="Marca un préstamo como devuelto, asigna la fecha de devolución "
                "y libera el dispositivo (is_available = true).",
    response_description="Préstamo devuelto correctamente",
    responses={
        404: {"description": "Préstamo no encontrado"},
        409: {"description": "El préstamo ya fue devuelto anteriormente"}
    }
)
def devolver_loan(loan_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return loan_service.devolver_loan(db, loan_id)

@router.get("/loans/details", response_model=list[LoanDetailResponse], status_code=200)
def detalles_loans(
    response: Response,
    db: Session = Depends(get_db),
    status: Optional[LoanStatusEnum] = Query(default=None),
    user_email: Optional[str] = Query(default=None, description="Buscar por email del usuario"),
    device_type: Optional[str] = Query(default=None, description="Buscar por tipo de dispositivo")
):
    agregar_cabeceras(response)
    return loan_service.obtener_detalles(db, status=status, user_email=user_email, device_type=device_type)