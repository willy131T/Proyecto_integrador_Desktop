from sqlalchemy import Column, String, Integer
from src.models.base import TimeStampedModel

class Inventario(TimeStampedModel):
    __tablename__ = "inventario"

    nombre = Column(String(150), index=True, nullable=False)
    cantidad = Column(Integer, default=0, nullable=False)
    categoria = Column(String(50), index=True, default="Materiales", nullable=False)

    def __repr__(self):
        return f"<Inventario(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, categoria='{self.categoria}')>"
