from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.base import TimeStampedModel

class Cita(TimeStampedModel):
    __tablename__ = "citas"

    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    nombre_paciente = Column(String(150), index=True, nullable=False)
    doctor = Column(String(100), index=True, nullable=False)
    fecha = Column(String(20), index=True, nullable=False)  # Formato DD/MM/YYYY
    hora = Column(String(10), nullable=False)               # Formato HH:MM
    motivo = Column(String(255), nullable=False)
    estado = Column(String(30), default="Pendiente", nullable=False)  # Pendiente, Completada, Cancelada

    def __repr__(self):
        return f"<Cita(id={self.id}, paciente='{self.nombre_paciente}', doctor='{self.doctor}', fecha='{self.fecha} {self.hora}')>"
