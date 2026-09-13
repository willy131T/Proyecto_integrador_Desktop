from datetime import datetime
from typing import List
from config.database import get_db
from src.models.diagnostico import Diagnostico
from src.services.paciente_service import PacienteService

class DiagnosticoService:
    @staticmethod
    def insertar_diagnostico(nombre_paciente: str, cita_info: str, procedimiento: str, medicamentos: str, fecha: str = None) -> bool:
        if not fecha:
            fecha = datetime.now().strftime("%d/%m/%Y")

        with get_db() as db:
            nuevo = Diagnostico(
                nombre_paciente=nombre_paciente.strip(),
                cita_info=cita_info.strip(),
                procedimiento=procedimiento.strip(),
                medicamentos=medicamentos.strip() if medicamentos else "Ninguno",
                fecha=fecha.strip()
            )
            db.add(nuevo)

        # Actualiza el tratamiento visible para el paciente
        tratamiento_resumen = f"📅 {cita_info}\n🦷 Proc: {procedimiento}"
        if medicamentos and medicamentos.strip():
            tratamiento_resumen += f"\n💊 Receta: {medicamentos.strip()}"
        PacienteService.actualizar_tratamiento(nombre_paciente, tratamiento_resumen)

        return True

    @staticmethod
    def obtener_diagnosticos_por_paciente(nombre_paciente: str) -> List[dict]:
        with get_db() as db:
            diag = db.query(Diagnostico).filter(
                Diagnostico.nombre_paciente.ilike(nombre_paciente.strip())
            ).order_by(Diagnostico.id.desc()).all()
            return [
                {
                    "id": d.id,
                    "paciente": d.nombre_paciente,
                    "cita_info": d.cita_info or "Consulta General",
                    "procedimiento": d.procedimiento,
                    "medicamentos": d.medicamentos or "Ninguno",
                    "fecha": d.fecha
                }
                for d in diag
            ]
