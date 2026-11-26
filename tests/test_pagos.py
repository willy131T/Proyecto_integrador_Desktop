import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.main import app
from src.services.pago_service import PagoService
from src.services.pdf_service import PDFService
from src.services.export_service import ExportService
from src.services.auth_service import AuthService

client = TestClient(app)


def test_pago_service_crud_y_resumen():
    creado = PagoService.registrar_pago(
        nombre_paciente="Paciente QA",
        concepto="Profilaxis QA",
        monto=500.0,
        metodo_pago="Tarjeta",
        estado="Pendiente",
        fecha="26/11/2026",
    )
    assert creado["id"] > 0
    assert creado["estado"] == "Pendiente"

    resumen = PagoService.obtener_resumen_financiero("Paciente QA")
    assert resumen["total_pendiente"] >= 500.0

    assert PagoService.marcar_como_pagado(creado["id"], metodo_pago="Efectivo") is True
    assert PagoService.eliminar_pago(creado["id"]) is True


def test_pago_validacion_monto_invalido():
    with pytest.raises(ValueError):
        PagoService.registrar_pago("Paciente QA", "Concepto", -50.0)


def test_api_pagos_flujo_completo():
    r_post = client.post(
        "/api/pagos",
        json={
            "nombre_paciente": "William Eduardo Antonio Marcelo",
            "concepto": "Consulta QA API",
            "monto": 350.0,
            "metodo_pago": "Efectivo",
            "estado": "Pendiente",
        },
    )
    assert r_post.status_code == 200
    pago_id = r_post.json()["pago"]["id"]

    r_pac = client.get("/api/pagos/paciente/William Eduardo Antonio Marcelo")
    assert r_pac.status_code == 200
    assert "saldo_pendiente" in r_pac.json()

    r_put = client.put(f"/api/pagos/{pago_id}/pagar")
    assert r_put.status_code == 200

    r_del = client.delete(f"/api/pagos/{pago_id}")
    assert r_del.status_code == 200


def test_recibo_pago_pdf():
    ruta = PDFService.generar_recibo_pago(
        paciente_nombre="Paciente Recibo",
        concepto="Resina Dental",
        monto=750.0,
        metodo_pago="Transferencia",
        estado="Pagado",
        fecha="26/11/2026",
        folio="QA-100",
    )
    assert Path(ruta).exists()
    os.remove(ruta)


def test_exportacion_csv_y_bi():
    stats = ExportService.obtener_estadisticas_bi()
    assert "total_citas" in stats
    assert "resumen_financiero" in stats

    csv_citas = ExportService.exportar_citas_csv()
    csv_inv = ExportService.exportar_inventario_csv()
    csv_pagos = ExportService.exportar_pagos_csv()
    for path in (csv_citas, csv_inv, csv_pagos):
        assert Path(path).exists()
        os.remove(path)


def test_rbac_proteccion_admin_doctor():
    doctores = AuthService.obtener_doctores_detalle()
    admin = next((d for d in doctores if d.get("es_admin_principal")), None)
    assert admin is not None
    ok, msg = AuthService.eliminar_doctor(admin["id"], "admin_doctor")
    assert ok is False
    assert "administrador" in msg.lower() or "dueño" in msg.lower() or "sesión" in msg.lower()
