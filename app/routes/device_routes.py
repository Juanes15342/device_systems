from fastapi import APIRouter, Query, Response, Depends
from sqlalchemy.orm import Session
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service
from app.dependencies.user_dependencies import agregar_cabeceras
from app.dependencies.database_dependency import get_db
from typing import Optional

router = APIRouter()

@router.get("/devices", response_model=list[DeviceResponse], status_code=200)
def listar_devices(
    response: Response,
    db: Session = Depends(get_db),
    device_type: Optional[str] = Query(default=None),
    is_available: Optional[bool] = Query(default=None),
    brand: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Busca en name, serial_number, device_type")
):
    agregar_cabeceras(response)
    return device_service.obtener_todos(
        db, device_type=device_type, is_available=is_available, brand=brand, search=search
    )

@router.get("/devices/{device_id}", response_model=DeviceResponse, status_code=200)
def obtener_device(device_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return device_service.obtener_por_id(db, device_id)

@router.post("/devices", response_model=DeviceResponse, status_code=201)
def crear_device(device: DeviceCreate, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return device_service.crear_device(db, device)

@router.put("/devices/{device_id}", response_model=DeviceResponse, status_code=200)
def actualizar_device(device_id: int, device: DeviceCreate, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return device_service.actualizar_device(db, device_id, device)

@router.patch("/devices/{device_id}", response_model=DeviceResponse, status_code=200)
def actualizar_parcial(device_id: int, datos: DeviceUpdate, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    return device_service.actualizar_parcial(db, device_id, datos)

@router.delete("/devices/{device_id}", status_code=204)
def eliminar_device(device_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_cabeceras(response)
    device_service.eliminar_device(db, device_id)