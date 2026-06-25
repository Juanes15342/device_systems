from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class LoanStatusEnum(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"

class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")
    status: LoanStatusEnum = LoanStatusEnum.active

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "device_id": 3,
                "status": "active"
            }
        }
    }

class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = None
    status: Optional[LoanStatusEnum] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: LoanStatusEnum

    model_config = {"from_attributes": True}


# ─── Schemas resumidos para mostrar dentro del detalle ───────
class UserBasicInfo(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}

class DeviceBasicInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


# ─── Respuesta con información relacionada (joins) ───────────
class LoanDetailResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: LoanStatusEnum
    user: UserBasicInfo
    device: DeviceBasicInfo

    model_config = {"from_attributes": True}