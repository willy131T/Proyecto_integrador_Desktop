from sqlalchemy import Column, String, Text
from src.models.base import TimeStampedModel

class Diagnostico(TimeStampedModel):
    __tablename__ = "diagnosticos"

    nombre_paciente = Column(String(150), index=True, nullable=False)
    cita_info = Column(String(255), nullable=True)
    procedimiento = Column(Text, nullable=False)
    medicamentos = Column(Text, nullable=True)
    fecha = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Diagnostico(id={self.id}, paciente='{self.nombre_paciente}', fecha='{self.fecha}')>"
