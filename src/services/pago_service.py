from datetime import datetime
from typing import Dict, List, Optional
from config.database import get_db
from src.models.pago import Pago

METODOS_VALIDOS = {"Efectivo", "Tarjeta", "Transferencia"}
ESTADOS_VALIDOS = {"Pagado", "Pendiente"}


class PagoService:
    @staticmethod
    def _serialize(p: Pago) -> Dict:
        return {
            "id": p.id,
            "id_cita": p.id_cita,
            "nombre_paciente": p.nombre_paciente,
            "concepto": p.concepto,
            "monto": round(float(p.monto), 2),
            "metodo_pago": p.metodo_pago,
            "estado": p.estado,
            "fecha": p.fecha,
        }

    @staticmethod
    def registrar_pago(
        nombre_paciente: str,
        concepto: str,
        monto: float,
        metodo_pago: str = "Efectivo",
        estado: str = "Pagado",
        fecha: Optional[str] = None,
        id_cita: Optional[int] = None,
    ) -> Dict:
        if float(monto) <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        if metodo_pago not in METODOS_VALIDOS:
            raise ValueError(f"Método de pago inválido: {metodo_pago}")
        if estado not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado de pago inválido: {estado}")

        fecha_val = fecha or datetime.now().strftime("%d/%m/%Y")
        with get_db() as db:
            nuevo = Pago(
                id_cita=id_cita,
                nombre_paciente=nombre_paciente.strip(),
                concepto=concepto.strip(),
                monto=round(float(monto), 2),
                metodo_pago=metodo_pago,
                estado=estado,
                fecha=fecha_val,
            )
            db.add(nuevo)
            db.flush()
            return PagoService._serialize(nuevo)

    @staticmethod
    def obtener_todos_los_pagos(estado: Optional[str] = None) -> List[Dict]:
        with get_db() as db:
            query = db.query(Pago)
            if estado and estado != "Todos":
                query = query.filter(Pago.estado == estado)
            pagos = query.order_by(Pago.id.desc()).all()
            return [PagoService._serialize(p) for p in pagos]

    @staticmethod
    def obtener_pagos_por_paciente(nombre_paciente: str) -> List[Dict]:
        with get_db() as db:
            pagos = (
                db.query(Pago)
                .filter(Pago.nombre_paciente == nombre_paciente)
                .order_by(Pago.id.desc())
                .all()
            )
            return [PagoService._serialize(p) for p in pagos]

    @staticmethod
    def marcar_como_pagado(id_pago: int, metodo_pago: Optional[str] = None) -> bool:
        with get_db() as db:
            pago = db.query(Pago).filter(Pago.id == id_pago).first()
            if not pago:
                return False
            pago.estado = "Pagado"
            if metodo_pago and metodo_pago in METODOS_VALIDOS:
                pago.metodo_pago = metodo_pago
            return True

    @staticmethod
    def eliminar_pago(id_pago: int) -> bool:
        with get_db() as db:
            pago = db.query(Pago).filter(Pago.id == id_pago).first()
            if not pago:
                return False
            db.delete(pago)
            return True

    @staticmethod
    def obtener_resumen_financiero(nombre_paciente: Optional[str] = None) -> Dict:
        pagos = (
            PagoService.obtener_pagos_por_paciente(nombre_paciente)
            if nombre_paciente
            else PagoService.obtener_todos_los_pagos()
        )
        total_recaudado = round(sum(p["monto"] for p in pagos if p["estado"] == "Pagado"), 2)
        total_pendiente = round(sum(p["monto"] for p in pagos if p["estado"] == "Pendiente"), 2)
        por_metodo: Dict[str, float] = {"Efectivo": 0.0, "Tarjeta": 0.0, "Transferencia": 0.0}
        for p in pagos:
            if p["estado"] == "Pagado":
                por_metodo[p["metodo_pago"]] = round(
                    por_metodo.get(p["metodo_pago"], 0.0) + p["monto"], 2
                )
        return {
            "total_recaudado": total_recaudado,
            "total_pendiente": total_pendiente,
            "cantidad_pagos": len(pagos),
            "por_metodo": por_metodo,
        }
