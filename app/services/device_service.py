from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate

def crear_device(db: Session, device: DeviceCreate):
    existente = db.query(Device).filter(Device.serial_number == device.serial_number).first()
    if existente:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    nuevo = Device(**device.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_todos(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None
):
    query = db.query(Device)

    if device_type is not None:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand is not None:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search is not None:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.device_type.ilike(f"%{search}%")
            )
        )

    return query.all()

def obtener_por_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id {device_id} no encontrado")
    return device

def actualizar_device(db: Session, device_id: int, datos: DeviceCreate):
    device = obtener_por_id(db, device_id)
    duplicado = db.query(Device).filter(
        Device.serial_number == datos.serial_number,
        Device.id != device_id
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for campo, valor in datos.model_dump().items():
        setattr(device, campo, valor)
    db.commit()
    db.refresh(device)
    return device

def actualizar_parcial(db: Session, device_id: int, datos: DeviceUpdate):
    campos = datos.model_dump(exclude_none=True)
    if not campos:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo para actualizar")
    device = obtener_por_id(db, device_id)
    if "serial_number" in campos:
        duplicado = db.query(Device).filter(
            Device.serial_number == campos["serial_number"],
            Device.id != device_id
        ).first()
        if duplicado:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for campo, valor in campos.items():
        setattr(device, campo, valor)
    db.commit()
    db.refresh(device)
    return device

def eliminar_device(db: Session, device_id: int):
    device = obtener_por_id(db, device_id)
    db.delete(device)
    db.commit()
    return {"message": f"Dispositivo con id {device_id} eliminado correctamente"}