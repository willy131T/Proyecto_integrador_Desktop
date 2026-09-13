from typing import Optional
from pydantic import BaseModel, Field

class CitaBase(BaseModel):
    nombre_paciente: str = Field(..., min_length=2)
    doctor: str = Field(..., min_length=2)
    fecha: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")
    hora: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    motivo: str = Field(..., min_length=2)
    estado: str = Field(default="Pendiente")

class CitaCreate(CitaBase):
    id_paciente: Optional[int] = None

class CitaResponse(CitaBase):
    id: int
    id_paciente: Optional[int] = None

    class Config:
        from_attributes = True
