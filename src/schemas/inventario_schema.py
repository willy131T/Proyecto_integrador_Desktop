from pydantic import BaseModel, Field

class InventarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    cantidad: int = Field(..., ge=0)
    categoria: str = Field(default="Materiales")

class InventarioCreate(InventarioBase):
    pass

class InventarioResponse(InventarioBase):
    id: int

    class Config:
        from_attributes = True
