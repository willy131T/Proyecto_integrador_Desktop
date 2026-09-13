import bcrypt
from typing import Optional, List
from config.database import get_db
from src.models.usuario import Usuario

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        # Respaldo de seguridad en caso de contraseñas legado en texto plano
        return plain_password == hashed_password

class AuthService:
    @staticmethod
    def iniciar_sesion(usuario_str: str, password_str: str) -> Optional[Usuario]:
        with get_db() as db:
            user = db.query(Usuario).filter(Usuario.usuario == usuario_str.strip()).first()
            if not user:
                return None
            if verify_password(password_str.strip(), user.password_hash):
                return user
            return None

    @staticmethod
    def registrar_paciente(nombre: str, usuario: str, password: str, edad: int, alergias: str = "Ninguna") -> bool:
        with get_db() as db:
            existente = db.query(Usuario).filter(Usuario.usuario == usuario.strip()).first()
            if existente:
                return False
            nuevo = Usuario(
                nombre=nombre.strip(),
                usuario=usuario.strip(),
                password_hash=hash_password(password.strip()),
                rol="paciente",
                edad=edad,
                alergias=alergias.strip() if alergias else "Ninguna",
                tratamiento="Sin tratamiento activo"
            )
            db.add(nuevo)
            return True

    @staticmethod
    def registrar_doctor(nombre: str, usuario: str, password: str) -> bool:
        with get_db() as db:
            existente = db.query(Usuario).filter(Usuario.usuario == usuario.strip()).first()
            if existente:
                return False
            nuevo = Usuario(
                nombre=nombre.strip(),
                usuario=usuario.strip(),
                password_hash=hash_password(password.strip()),
                rol="dentista",
                alergias="Ninguna",
                tratamiento=""
            )
            db.add(nuevo)
            return True

    @staticmethod
    def obtener_doctores() -> List[str]:
        with get_db() as db:
            doctores = db.query(Usuario).filter(Usuario.rol == "dentista").all()
            if not doctores:
                return ["Dr. Admin", "Dra. López", "Dr. Martínez"]
            return [d.nombre for d in doctores]

    @staticmethod
    def obtener_doctores_detalle() -> List[dict]:
        with get_db() as db:
            doctores = db.query(Usuario).filter(Usuario.rol == "dentista").order_by(Usuario.id.asc()).all()
            return [
                {
                    "id": d.id,
                    "nombre": d.nombre,
                    "usuario": d.usuario,
                    "es_admin_principal": d.usuario == "admin_doctor"
                }
                for d in doctores
            ]

    @staticmethod
    def eliminar_doctor(id_doctor: int, usuario_solicitante: str = "") -> tuple[bool, str]:
        """Elimina un doctor. Protege al administrador principal y previene auto-eliminación."""
        with get_db() as db:
            doctor = db.query(Usuario).filter(Usuario.id == id_doctor, Usuario.rol == "dentista").first()
            if not doctor:
                return False, "El doctor especificado no existe."

            # Proteger cuenta raíz del dueño
            if doctor.usuario == "admin_doctor":
                return False, "No se puede eliminar la cuenta del Administrador Principal (Dueño)."

            # Prevenir auto-eliminación
            if usuario_solicitante and doctor.usuario == usuario_solicitante:
                return False, "No puedes eliminar tu propia cuenta mientras tienes la sesión activa."

            db.delete(doctor)
            return True, f"El doctor '{doctor.nombre}' fue dado de baja exitosamente."
