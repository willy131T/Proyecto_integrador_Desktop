from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from src.services.cita_service import CitaService

router = APIRouter(prefix="/api/citas", tags=["Citas y Agenda"])

class AgendarCitaDTO(BaseModel):
    nombre_paciente: str
    doctor: str
    fecha: str = Field(..., description="Formato DD/MM/YYYY")
    hora: str = Field(..., description="Formato HH:MM")
    motivo: str
    id_paciente: Optional[int] = None

@router.get("")
def listar_todas_las_citas():
    return {"citas": CitaService.obtener_todas_las_citas()}

@router.get("/paciente/{nombre}")
def obtener_citas_paciente(nombre: str):
    return {"citas": CitaService.obtener_citas_por_paciente(nombre)}

@router.get("/proxima/{nombre}")
def obtener_proxima_cita(nombre: str):
    cita = CitaService.obtener_proxima_cita_paciente(nombre)
    return {"proxima_cita": cita}

@router.post("")
def agendar_cita(data: AgendarCitaDTO):
    # Verificación de colisión de horario
    if CitaService.verificar_disponibilidad(data.doctor, data.fecha, data.hora):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El {data.doctor} ya tiene una cita reservada el {data.fecha} a las {data.hora}."
        )

    ok = CitaService.agendar_cita(
        nombre_paciente=data.nombre_paciente,
        doctor=data.doctor,
        fecha=data.fecha,
        hora=data.hora,
        motivo=data.motivo,
        id_paciente=data.id_paciente
    )
    if not ok:
        raise HTTPException(status_code=400, detail="Error al agendar la cita")

    return {"success": True, "mensaje": "Cita agendada correctamente"}

@router.put("/{id_cita}/completar")
def completar_cita(id_cita: int):
    ok = CitaService.cambiar_estado_cita(id_cita, "Completada")
    if not ok:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"success": True, "mensaje": "Cita marcada como completada"}

@router.delete("/{id_cita}")
def cancelar_cita(id_cita: int):
    ok = CitaService.eliminar_cita(id_cita)
    if not ok:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"success": True, "mensaje": "Cita cancelada exitosamente"}