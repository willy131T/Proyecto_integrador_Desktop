from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.paciente_service import PacienteService
from src.services.diagnostico_service import DiagnosticoService

router = APIRouter(prefix="/api/pacientes", tags=["Pacientes y Expedientes"])

class DiagnosticoDTO(BaseModel):
    cita_info: str
    procedimiento: str
    medicamentos: Optional[str] = "Ninguno"
    fecha: Optional[str] = None

@router.get("")
def listar_pacientes(buscar: Optional[str] = None):
    return {"pacientes": PacienteService.obtener_pacientes(filtro=buscar)}

@router.get("/{nombre}")
def obtener_detalle_paciente(nombre: str):
    pac = PacienteService.obtener_paciente_por_nombre(nombre)
    if not pac:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"paciente": pac}

@router.get("/{nombre}/diagnosticos")
def obtener_historial_diagnosticos(nombre: str):
    diagnosticos = DiagnosticoService.obtener_diagnosticos_por_paciente(nombre)
    return {"diagnosticos": diagnosticos}

@router.post("/{nombre}/diagnosticos")
def registrar_diagnostico(nombre: str, data: DiagnosticoDTO):
    ok = DiagnosticoService.insertar_diagnostico(
        nombre_paciente=nombre,
        cita_info=data.cita_info,
        procedimiento=data.procedimiento,
        medicamentos=data.medicamentos or "Ninguno",
        fecha=data.fecha
    )
    if not ok:
        raise HTTPException(status_code=400, detail="Error al registrar diagnóstico")
    return {"success": True, "mensaje": "Diagnóstico guardado y tratamiento actualizado"}