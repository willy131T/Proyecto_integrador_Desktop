from sqlalchemy import Column, String, Integer, Float, ForeignKey
from src.models.base import TimeStampedModel


class Pago(TimeStampedModel):
    __tablename__ = "pagos"

    id_cita = Column(Integer, ForeignKey("citas.id"), nullable=True)
    nombre_paciente = Column(String(150), index=True, nullable=False)
    concepto = Column(String(255), nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(40), default="Efectivo", nullable=False)  # Efectivo, Tarjeta, Transferencia
    estado = Column(String(30), default="Pagado", nullable=False)  # Pagado, Pendiente
    fecha = Column(String(20), index=True, nullable=False)  # Formato DD/MM/YYYY

    def __repr__(self):
        return f"<Pago(id={self.id}, paciente='{self.nombre_paciente}', monto={self.monto}, estado='{self.estado}')>"
