import os
import uuid
import pytest
from src.services.auth_service import AuthService, hash_password, verify_password
from src.services.cita_service import CitaService
from src.services.inventario_service import InventarioService
from src.services.diagnostico_service import DiagnosticoService
from src.services.pdf_service import PDFService

def test_password_hashing():
    pwd = "secreto123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("incorrecto", hashed) is False

def test_auth_login():
    user = AuthService.iniciar_sesion("admin_doctor", "12345")
    assert user is not None
    assert user.rol == "dentista"

    user_paciente = AuthService.iniciar_sesion("william_p", "12345")
    assert user_paciente is not None
    assert user_paciente.rol == "paciente"

    user_fail = AuthService.iniciar_sesion("admin_doctor", "wrong_pwd")
    assert user_fail is None

def test_cita_collision():
    # Usar hora aleatoria para asegurar aislamiento de pruebas
    fec = "28/12/2026"
    hor = f"{uuid.uuid4().hex[:2]}:00"[:5]
    doc = "Dr. Martínez"
    
    ok1 = CitaService.agendar_cita("Paciente Aislamiento", doc, fec, hor, "Consulta prueba")
    assert ok1 is True

    # Intentar agendar en la misma fecha y hora con el mismo doctor -> debe bloquear por colisión
    ok2 = CitaService.agendar_cita("Paciente Bloqueado", doc, fec, hor, "Consulta colisión")
    assert ok2 is False

def test_inventario_crud():
    inv = InventarioService.obtener_inventario()
    assert len(inv) > 0

    alertas = InventarioService.obtener_alertas_stock_bajo(umbral=15)
    assert isinstance(alertas, list)

def test_pdf_generation():
    pdf_path = PDFService.generar_receta_medica(
        paciente_nombre="Paciente Prueba",
        doctor_nombre="Dr. Admin",
        procedimiento="Limpieza con ultrasonido",
        medicamentos="Ibuprofeno 400mg cada 8 horas por 3 días"
    )
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith(".pdf")

def test_gestionar_doctores():
    # 1. Registrar doctor temporal
    doc_user = f"doc_temp_{uuid.uuid4().hex[:6]}"
    ok_reg = AuthService.registrar_doctor("Doctor Temporal", doc_user, "12345")
    assert ok_reg is True

    # 2. Obtener lista con detalles y verificar que existe
    docs = AuthService.obtener_doctores_detalle()
    creado = next((d for d in docs if d["usuario"] == doc_user), None)
    assert creado is not None

    # 3. Intentar eliminar al Admin Principal -> debe ser rechazado
    admin = next(d for d in docs if d["usuario"] == "admin_doctor")
    ok_del_admin, msg_admin = AuthService.eliminar_doctor(admin["id"], "admin_doctor")
    assert ok_del_admin is False
    assert "Dueño" in msg_admin

    # 4. Intentar auto-eliminarse -> debe ser rechazado
    ok_self, msg_self = AuthService.eliminar_doctor(creado["id"], doc_user)
    assert ok_self is False
    assert "propia cuenta" in msg_self

    # 5. Eliminar doctor temporal correctamente por otro admin
    ok_del, msg_del = AuthService.eliminar_doctor(creado["id"], "admin_doctor")
    assert ok_del is True
    assert "exitosamente" in msg_del