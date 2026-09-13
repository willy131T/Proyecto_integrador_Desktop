from typing import Optional
from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    usuario: str = Field(..., min_length=3, max_length=50)
    rol: str = Field(default="paciente")
    edad: Optional[int] = Field(default=None, ge=0, le=120)
    alergias: Optional[str] = "Ninguna"
    tratamiento: Optional[str] = "Sin tratamiento"

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=4)

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    usuario: str
    password: str
