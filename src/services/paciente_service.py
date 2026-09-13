from typing import List, Optional
from config.database import get_db
from src.models.paciente import Paciente

class PacienteService:
    @staticmethod
    def obtener_pacientes(filtro: Optional[str] = None) -> List[dict]:
        with get_db() as db:
            query = db.query(Paciente)
            if filtro:
                query = query.filter(Paciente.nombre.ilike(f"%{filtro.strip()}%"))
            pacientes = query.order_by(Paciente.nombre.asc()).all()
            return [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "edad": p.edad or 0,
                    "telefono": p.telefono or "No registrado",
                    "correo": p.correo or "No registrado",
                    "alergias": p.alergias or "Ninguna",
                    "tratamiento": p.tratamiento or "Sin tratamiento registrado"
                }
                for p in pacientes
            ]

    @staticmethod
    def obtener_paciente_por_nombre(nombre: str) -> Optional[dict]:
        with get_db() as db:
            p = db.query(Paciente).filter(Paciente.nombre.ilike(nombre.strip())).first()
            if not p:
                return None
            return {
                "id": p.id,
                "nombre": p.nombre,
                "edad": p.edad or 0,
                "telefono": p.telefono or "No registrado",
                "correo": p.correo or "No registrado",
                "alergias": p.alergias or "Ninguna",
                "tratamiento": p.tratamiento or "Sin tratamiento registrado"
            }

    @staticmethod
    def registrar_o_actualizar_paciente(nombre: str, edad: int, alergias: str, tratamiento: str = "Sin tratamiento", telefono: str = "", correo: str = "") -> bool:
        with get_db() as db:
            p = db.query(Paciente).filter(Paciente.nombre.ilike(nombre.strip())).first()
            if p:
                p.edad = edad
                p.alergias = alergias
                if tratamiento:
                    p.tratamiento = tratamiento
                if telefono:
                    p.telefono = telefono
                if correo:
                    p.correo = correo
            else:
                nuevo = Paciente(
                    nombre=nombre.strip(),
                    edad=edad,
                    alergias=alergias.strip() if alergias else "Ninguna",
                    tratamiento=tratamiento,
                    telefono=telefono,
                    correo=correo
                )
                db.add(nuevo)
            return True

    @staticmethod
    def actualizar_tratamiento(nombre: str, nuevo_tratamiento: str) -> bool:
        with get_db() as db:
            p = db.query(Paciente).filter(Paciente.nombre.ilike(nombre.strip())).first()
            if p:
                p.tratamiento = nuevo_tratamiento
                return True
            return False
