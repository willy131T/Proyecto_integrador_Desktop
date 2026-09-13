from sqlalchemy import Column, String, Integer, Text
from src.models.base import TimeStampedModel

class Usuario(TimeStampedModel):
    __tablename__ = "usuarios"

    nombre = Column(String(150), nullable=False)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="paciente", nullable=False)  # 'dentista' o 'paciente'
    edad = Column(Integer, nullable=True)
    alergias = Column(Text, default="Ninguna")
    tratamiento = Column(Text, default="Sin tratamiento")

    def __repr__(self):
        return f"<Usuario(id={self.id}, usuario='{self.usuario}', rol='{self.rol}')>"
