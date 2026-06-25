from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate
from sqlalchemy import and_, or_

def crear_loan(db: Session, loan: LoanCreate):
    usuario = db.query(User).filter(User.id == loan.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {loan.user_id} no encontrado")

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id {loan.device_id} no encontrado")

    if not device.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible para préstamo")

    nuevo_loan = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id,
        status=loan.status,
        loan_date=datetime.utcnow()
    )
    db.add(nuevo_loan)
    device.is_available = False
    db.commit()
    db.refresh(nuevo_loan)
    return nuevo_loan

def obtener_todos(db: Session, status: str = None):
    query = db.query(Loan)
    if status is not None:
        query = query.filter(Loan.status == status)
    return query.all()

def obtener_por_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con id {loan_id} no encontrado")
    return loan

def devolver_loan(db: Session, loan_id: int):
    loan = obtener_por_id(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="Este préstamo ya fue devuelto anteriormente")

    loan.status = "returned"
    loan.return_date = datetime.utcnow()

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan

def obtener_detalles(db: Session, status: str = None, user_email: str = None, device_type: str = None):
    query = db.query(Loan).join(User, Loan.user_id == User.id).join(Device, Loan.device_id == Device.id)
    condiciones = []
    if status is not None:
        condiciones.append(Loan.status == status)
    if user_email is not None:
        condiciones.append(User.email.ilike(f"%{user_email}%"))
    if device_type is not None:
        condiciones.append(Device.device_type.ilike(f"%{device_type}%"))
    if condiciones:
        query = query.filter(and_(*condiciones))
    return query.all()

def obtener_loans_por_usuario(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def obtener_loans_por_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id {device_id} no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()