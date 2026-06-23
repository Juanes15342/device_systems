from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del dispositivo")
    serial_number: str = Field(..., min_length=3, description="Número de serie único")
    device_type: str = Field(..., description="Ej: laptop, tablet, proyector, cámara, router, monitor")
    brand: Optional[str] = None
    is_available: bool = True

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    serial_number: Optional[str] = Field(default=None, min_length=3)
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}