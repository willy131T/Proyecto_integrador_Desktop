from sqlalchemy import Column, String, Integer, Text
from src.models.base import TimeStampedModel

class Paciente(TimeStampedModel):
    __tablename__ = "pacientes"

    nombre = Column(String(150), index=True, nullable=False)
    edad = Column(Integer, nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(120), nullable=True)
    alergias = Column(Text, default="Ninguna")
    tratamiento = Column(Text, default="Sin tratamiento")

    def __repr__(self):
        return f"<Paciente(id={self.id}, nombre='{self.nombre}')>"
