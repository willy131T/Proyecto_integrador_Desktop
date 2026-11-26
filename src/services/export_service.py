import csv
from collections import Counter
from datetime import datetime
from typing import Dict
from config.settings import REPORTS_DIR
from src.services.cita_service import CitaService
from src.services.inventario_service import InventarioService
from src.services.pago_service import PagoService


class ExportService:
    @staticmethod
    def exportar_citas_csv() -> str:
        citas = CitaService.obtener_todas_las_citas()
        filepath = REPORTS_DIR / f"Reporte_Citas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Paciente", "Doctor", "Fecha", "Hora", "Motivo", "Estado"])
            for c in citas:
                writer.writerow([c["id"], c["paciente"], c["doctor"], c["fecha"], c["hora"], c["motivo"], c["estado"]])
        return str(filepath)

    @staticmethod
    def exportar_inventario_csv() -> str:
        items = InventarioService.obtener_inventario()
        filepath = REPORTS_DIR / f"Reporte_Inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Insumo", "Categoria", "Cantidad", "Nivel"])
            for m in items:
                nivel = "CRITICO" if m["cantidad"] <= 15 else "NORMAL"
                writer.writerow([m["id"], m["nombre"], m["categoria"], m["cantidad"], nivel])
        return str(filepath)

    @staticmethod
    def exportar_pagos_csv() -> str:
        pagos = PagoService.obtener_todos_los_pagos()
        filepath = REPORTS_DIR / f"Reporte_Pagos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Paciente", "Concepto", "Monto", "Metodo", "Estado", "Fecha"])
            for p in pagos:
                writer.writerow([p["id"], p["nombre_paciente"], p["concepto"], p["monto"], p["metodo_pago"], p["estado"], p["fecha"]])
        return str(filepath)

    @staticmethod
    def obtener_estadisticas_bi() -> Dict:
        citas = CitaService.obtener_todas_las_citas()
        inventario = InventarioService.obtener_inventario()
        resumen_fin = PagoService.obtener_resumen_financiero()

        citas_por_doctor = dict(Counter(c["doctor"] for c in citas))
        citas_por_estado = dict(Counter(c["estado"] for c in citas))
        alertas_stock = [m for m in inventario if m["cantidad"] <= 15]

        return {
            "total_citas": len(citas),
            "citas_por_doctor": citas_por_doctor,
            "citas_por_estado": citas_por_estado,
            "resumen_financiero": resumen_fin,
            "total_insumos": len(inventario),
            "alertas_stock": alertas_stock,
        }
