import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.database import get_db, init_db
from src.models.usuario import Usuario
from src.models.paciente import Paciente
from src.models.cita import Cita
from src.models.inventario import Inventario
from src.models.diagnostico import Diagnostico
from src.services.auth_service import hash_password

def seed_database():
    print("🌱 Inicializando base de datos y cargando datos semilla...")
    init_db()

    with get_db() as db:
        # 1. Cuentas de Doctores
        doctores = [
            ("Doctor Admin", "admin_doctor", "12345", "dentista"),
            ("Dra. López", "dra_lopez", "12345", "dentista"),
            ("Dr. Martínez", "dr_martinez", "12345", "dentista"),
        ]
        for nombre, user, pwd, rol in doctores:
            if not db.query(Usuario).filter(Usuario.usuario == user).first():
                db.add(Usuario(
                    nombre=nombre,
                    usuario=user,
                    password_hash=hash_password(pwd),
                    rol=rol,
                    alergias="Ninguna",
                    tratamiento=""
                ))

        # 2. Cuentas de Pacientes
        pacientes_usuarios = [
            ("William Eduardo Antonio Marcelo", "william_p", "12345", 19, "Ninguna", "📅 Cita: 20/07/2026 [16:00] - Ortodoncia\n🦷 Proc: Cambio de ligas y ajuste de arco.\n💊 Receta: Ninguno"),
            ("Andrés", "andres_p", "12345", 20, "Ninguna", "📅 Cita: 01/08/2026 [09:00] - Revisión general\n🦷 Proc: Revisión de rutina\n💊 Receta: Ninguno"),
            ("Sofi", "sofi_p", "12345", 19, "Penicilina", "Sin tratamientos activos"),
        ]
        for nombre, user, pwd, edad, alergias, trat in pacientes_usuarios:
            if not db.query(Usuario).filter(Usuario.usuario == user).first():
                db.add(Usuario(
                    nombre=nombre,
                    usuario=user,
                    password_hash=hash_password(pwd),
                    rol="paciente",
                    edad=edad,
                    alergias=alergias,
                    tratamiento=trat
                ))

        # 3. Directorio de Pacientes / Expedientes
        pacientes_directorio = [
            ("William Eduardo Antonio Marcelo", 19, "5551234567", "william@test.com", "Ninguna", "Ortodoncia activa"),
            ("Andrés", 20, "5559876543", "andres@test.com", "Ninguna", "Resina"),
            ("Sofi", 19, "5554567890", "sofi@test.com", "Penicilina", "Revisión General"),
        ]
        for nombre, edad, tel, mail, alergias, trat in pacientes_directorio:
            if not db.query(Paciente).filter(Paciente.nombre == nombre).first():
                db.add(Paciente(
                    nombre=nombre,
                    edad=edad,
                    telefono=tel,
                    correo=mail,
                    alergias=alergias,
                    tratamiento=trat
                ))

        # 4. Citas Históricas
        citas_iniciales = [
            (1, "William Eduardo Antonio Marcelo", "Dra. López", "10/05/2026", "10:00", "Limpieza dental (Profilaxis)", "Completada"),
            (1, "William Eduardo Antonio Marcelo", "Doctor Admin", "15/06/2026", "12:30", "Dolor agudo / Urgencia", "Completada"),
            (1, "William Eduardo Antonio Marcelo", "Dr. Martínez", "20/07/2026", "16:00", "Ortodoncia (Ajuste / Revision)", "Pendiente"),
            (2, "Andrés", "Doctor Admin", "01/08/2026", "09:00", "Revisión general", "Pendiente"),
        ]
        for pid, pnom, doc, fec, hor, mot, est in citas_iniciales:
            if not db.query(Cita).filter(Cita.nombre_paciente == pnom, Cita.fecha == fec, Cita.hora == hor).first():
                db.add(Cita(
                    id_paciente=pid,
                    nombre_paciente=pnom,
                    doctor=doc,
                    fecha=fec,
                    hora=hor,
                    motivo=mot,
                    estado=est
                ))

        # 5. Diagnósticos
        diagnosticos_iniciales = [
            ("William Eduardo Antonio Marcelo", "Cita: 10/05/2026 [10:00] - Limpieza dental", "Profilaxis ultrasónica y pulido coronal. Se detectó caries incipiente en molar 36.", "Enjuague con clorhexidina al 0.12% por 5 días", "10/05/2026"),
            ("William Eduardo Antonio Marcelo", "Cita: 15/06/2026 [12:30] - Dolor agudo / Urgencia", "Eliminación de tejido cariado en pieza 36 y colocación de resina compuesta tono A2.", "Ibuprofeno 400mg cada 8 hrs por 3 días", "15/06/2026"),
            ("William Eduardo Antonio Marcelo", "Cita: 20/07/2026 [16:00] - Ortodoncia", "Cambio de ligas y ajuste de arco superior e inferior. Evolución favorable.", "Ninguno", "20/07/2026"),
            ("Andrés", "Cita: 01/08/2026 [09:00] - Revisión general", "Revisión de rutina, toma de radiografía panorámica. Sin alteraciones visibles.", "Ninguno", "01/08/2026"),
        ]
        for pnom, cinfo, proc, med, fec in diagnosticos_iniciales:
            if not db.query(Diagnostico).filter(Diagnostico.nombre_paciente == pnom, Diagnostico.fecha == fec).first():
                db.add(Diagnostico(
                    nombre_paciente=pnom,
                    cita_info=cinfo,
                    procedimiento=proc,
                    medicamentos=med,
                    fecha=fec
                ))

        # 6. Catálogo de 23 Insumos de Inventario
        materiales = [
            ("Anestesia Local (Cárpules)", 150, "Medicamentos"),
            ("Ibuprofeno 400mg (Cajas)", 20, "Medicamentos"),
            ("Amoxicilina 500mg (Cajas)", 15, "Medicamentos"),
            ("Clorhexidina al 0.12% (Frascos)", 10, "Medicamentos"),
            ("Ketorolaco 10mg (Cajas)", 12, "Medicamentos"),
            ("Resina Compuesta A2 (Jeringas)", 30, "Materiales"),
            ("Resina Compuesta A3 (Jeringas)", 25, "Materiales"),
            ("Ionómero de Vidrio (Kits)", 12, "Materiales"),
            ("Ácido Grabador (Jeringas)", 18, "Materiales"),
            ("Adhesivo Dental (Frascos)", 15, "Materiales"),
            ("Cemento Quirúrgico", 8, "Materiales"),
            ("Guantes de Látex (Cajas)", 40, "Desechables"),
            ("Cubrebocas Tricapa (Cajas)", 50, "Desechables"),
            ("Eyectores de Saliva (Bolsas)", 25, "Desechables"),
            ("Algodón en Rollos (Bolsas)", 30, "Desechables"),
            ("Agujas Dentales Cortas (Cajas)", 15, "Desechables"),
            ("Baberos para Paciente (Paquetes)", 20, "Desechables"),
            ("Espejos Bucales", 20, "Instrumental"),
            ("Exploradores Dentales", 15, "Instrumental"),
            ("Pinzas Algodoneras", 15, "Instrumental"),
            ("Jeringas Carpule", 10, "Instrumental"),
            ("Fórceps para Extracción", 8, "Instrumental"),
            ("Curetas periodontales", 12, "Instrumental")
        ]
        for nom, cant, cat in materiales:
            if not db.query(Inventario).filter(Inventario.nombre == nom).first():
                db.add(Inventario(nombre=nom, cantidad=cant, categoria=cat))

    print("✅ Carga masiva de datos iniciales completada exitosamente.")

if __name__ == "__main__":
    seed_database()
