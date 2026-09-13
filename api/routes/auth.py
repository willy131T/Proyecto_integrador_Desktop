from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.auth_service import AuthService
from src.services.paciente_service import PacienteService

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

class LoginDTO(BaseModel):
    usuario: str
    password: str

class RegistroPacienteDTO(BaseModel):
    nombre: str
    usuario: str
    password: str
    edad: int
    alergias: str = "Ninguna"

@router.post("/login")
def login(data: LoginDTO):
    user = AuthService.iniciar_sesion(data.usuario, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    return {
        "success": True,
        "usuario": {
            "id": user.id,
            "nombre": user.nombre,
            "usuario": user.usuario,
            "rol": user.rol,
            "edad": user.edad,
            "alergias": user.alergias,
            "tratamiento": user.tratamiento
        }
    }

@router.post("/registro-paciente")
def registrar_paciente(data: RegistroPacienteDTO):
    ok_user = AuthService.registrar_paciente(
        nombre=data.nombre,
        usuario=data.usuario,
        password=data.password,
        edad=data.edad,
        alergias=data.alergias
    )
    if not ok_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya se encuentra registrado."
        )

    # Actualizar o registrar en el directorio clínico de pacientes
    PacienteService.registrar_o_actualizar_paciente(
        nombre=data.nombre,
        edad=data.edad,
        alergias=data.alergias
    )

    return {"success": True, "mensaje": "Paciente registrado exitosamente"}

@router.get("/doctores")
def obtener_doctores():
    return {"doctores": AuthService.obtener_doctores()}

@router.get("/doctores/detalle")
def obtener_doctores_detalle():
    return {"doctores": AuthService.obtener_doctores_detalle()}

@router.delete("/doctores/{id_doctor}")
def eliminar_doctor(id_doctor: int, usuario_solicitante: str = ""):
    ok, mensaje = AuthService.eliminar_doctor(id_doctor, usuario_solicitante)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensaje)
    return {"success": True, "mensaje": mensaje}