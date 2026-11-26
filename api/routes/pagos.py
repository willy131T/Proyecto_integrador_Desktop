from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from src.schemas.pago_schema import PagoCreate
from src.services.pago_service import PagoService

router = APIRouter(prefix="/api/pagos", tags=["Finanzas y Pagos"])


@router.get("")
def listar_pagos(estado: Optional[str] = Query(default=None)):
    return {"pagos": PagoService.obtener_todos_los_pagos(estado=estado)}


@router.get("/resumen")
def obtener_resumen():
    return PagoService.obtener_resumen_financiero()


@router.get("/paciente/{nombre}")
def listar_pagos_paciente(nombre: str):
    pagos = PagoService.obtener_pagos_por_paciente(nombre)
    resumen = PagoService.obtener_resumen_financiero(nombre_paciente=nombre)
    return {
        "paciente": nombre,
        "pagos": pagos,
        "total_pagado": resumen["total_recaudado"],
        "saldo_pendiente": resumen["total_pendiente"],
    }


@router.post("")
def registrar_pago(data: PagoCreate):
    try:
        creado = PagoService.registrar_pago(
            nombre_paciente=data.nombre_paciente,
            concepto=data.concepto,
            monto=data.monto,
            metodo_pago=data.metodo_pago,
            estado=data.estado,
            fecha=data.fecha,
            id_cita=data.id_cita,
        )
        return {"success": True, "pago": creado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id_pago}/pagar")
def marcar_pago_liquidado(id_pago: int, metodo_pago: Optional[str] = Query(default=None)):
    ok = PagoService.marcar_como_pagado(id_pago, metodo_pago=metodo_pago)
    if not ok:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"success": True, "mensaje": "Pago marcado como liquidado"}


@router.delete("/{id_pago}")
def eliminar_pago(id_pago: int):
    ok = PagoService.eliminar_pago(id_pago)
    if not ok:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"success": True, "mensaje": "Registro de pago eliminado"}
