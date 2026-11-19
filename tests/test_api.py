import uuid
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert data["engine"] in ("sqlite", "postgresql")

def test_api_login_success():
    response = client.post("/api/auth/login", json={
        "usuario": "admin_doctor",
        "password": "12345"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["usuario"]["rol"] == "dentista"

def test_api_login_fail():
    response = client.post("/api/auth/login", json={
        "usuario": "admin_doctor",
        "password": "password_incorrecto"
    })
    assert response.status_code == 401

def test_api_citas_list():
    response = client.get("/api/citas")
    assert response.status_code == 200
    assert "citas" in response.json()

def test_api_citas_collision():
    fec = "31/12/2026"
    hor = f"{uuid.uuid4().hex[:2]}:00"[:5]
    doc = "Dr. Martínez"

    # Agendar primera vez -> 200
    r1 = client.post("/api/citas", json={
        "nombre_paciente": "Paciente API",
        "doctor": doc,
        "fecha": fec,
        "hora": hor,
        "motivo": "Revisión rutinaria"
    })
    assert r1.status_code == 200

    # Agendar segunda vez en el mismo horario con el mismo doctor -> 409 Conflict
    r2 = client.post("/api/citas", json={
        "nombre_paciente": "Otro Paciente API",
        "doctor": doc,
        "fecha": fec,
        "hora": hor,
        "motivo": "Revisión urgente"
    })
    assert r2.status_code == 409

def test_api_pacientes():
    response = client.get("/api/pacientes")
    assert response.status_code == 200
    assert len(response.json()["pacientes"]) > 0

def test_api_inventario():
    response = client.get("/api/inventario")
    assert response.status_code == 200
    assert len(response.json()["inventario"]) > 0

def test_api_doctores_gestion():
    res = client.get("/api/auth/doctores/detalle")
    assert res.status_code == 200
    assert "doctores" in res.json()
    assert len(res.json()["doctores"]) >= 3