from typing import List, Optional
from config.database import get_db
from src.models.cita import Cita

class CitaService:
    @staticmethod
    def verificar_disponibilidad(doctor: str, fecha: str, hora: str) -> bool:
        """Retorna True si el horario ya está ocupado por el doctor."""
        with get_db() as db:
            existente = db.query(Cita).filter(
                Cita.doctor == doctor.strip(),
                Cita.fecha == fecha.strip(),
                Cita.hora == hora.strip(),
                Cita.estado != "Cancelada"
            ).first()
            return existente is not None

    @staticmethod
    def agendar_cita(nombre_paciente: str, doctor: str, fecha: str, hora: str, motivo: str, id_paciente: Optional[int] = None) -> bool:
        if CitaService.verificar_disponibilidad(doctor, fecha, hora):
            return False  # Conflicto de horario

        with get_db() as db:
            nueva_cita = Cita(
                id_paciente=id_paciente,
                nombre_paciente=nombre_paciente.strip(),
                doctor=doctor.strip(),
                fecha=fecha.strip(),
                hora=hora.strip(),
                motivo=motivo.strip(),
                estado="Pendiente"
            )
            db.add(nueva_cita)
            return True

    @staticmethod
    def obtener_todas_las_citas() -> List[dict]:
        with get_db() as db:
            citas = db.query(Cita).order_by(Cita.id.desc()).all()
            return [
                {
                    "id": c.id,
                    "paciente": c.nombre_paciente,
                    "doctor": c.doctor,
                    "fecha": c.fecha,
                    "hora": c.hora,
                    "motivo": c.motivo,
                    "estado": c.estado
                }
                for c in citas
            ]

    @staticmethod
    def obtener_citas_por_paciente(nombre_paciente: str) -> List[dict]:
        with get_db() as db:
            citas = db.query(Cita).filter(Cita.nombre_paciente == nombre_paciente.strip()).order_by(Cita.id.desc()).all()
            return [
                {
                    "id": c.id,
                    "paciente": c.nombre_paciente,
                    "doctor": c.doctor,
                    "fecha": c.fecha,
                    "hora": c.hora,
                    "motivo": c.motivo,
                    "estado": c.estado
                }
                for c in citas
            ]

    @staticmethod
    def obtener_proxima_cita_paciente(nombre_paciente: str) -> Optional[dict]:
        with get_db() as db:
            cita = db.query(Cita).filter(
                Cita.nombre_paciente == nombre_paciente.strip(),
                Cita.estado == "Pendiente"
            ).order_by(Cita.id.desc()).first()
            if not cita:
                return None
            return {
                "id": cita.id,
                "paciente": cita.nombre_paciente,
                "doctor": cita.doctor,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "motivo": cita.motivo,
                "estado": cita.estado
            }

    @staticmethod
    def eliminar_cita(id_cita: int) -> bool:
        with get_db() as db:
            cita = db.query(Cita).filter(Cita.id == id_cita).first()
            if cita:
                db.delete(cita)
                return True
            return False

    @staticmethod
    def cambiar_estado_cita(id_cita: int, nuevo_estado: str) -> bool:
        with get_db() as db:
            cita = db.query(Cita).filter(Cita.id == id_cita).first()
            if cita:
                cita.estado = nuevo_estado
                return True
            return False
