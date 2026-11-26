from typing import Optional, Literal
from pydantic import BaseModel, Field


class PagoCreate(BaseModel):
    nombre_paciente: str = Field(..., min_length=2)
    concepto: str = Field(..., min_length=2)
    monto: float = Field(..., gt=0)
    metodo_pago: Literal["Efectivo", "Tarjeta", "Transferencia"] = "Efectivo"
    estado: Literal["Pagado", "Pendiente"] = "Pagado"
    fecha: Optional[str] = None
    id_cita: Optional[int] = None


class PagoResponse(BaseModel):
    id: int
    id_cita: Optional[int] = None
    nombre_paciente: str
    concepto: str
    monto: float
    metodo_pago: str
    estado: str
    fecha: str

    class Config:
        from_attributes = True
