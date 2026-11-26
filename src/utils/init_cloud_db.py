import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.database import check_db_connection, get_db
from src.models.usuario import Usuario
from src.models.paciente import Paciente
from src.models.cita import Cita
from src.models.inventario import Inventario
from src.models.diagnostico import Diagnostico
from src.models.pago import Pago
from src.utils.seed_data import seed_database


def main():
    """Inicializa tablas, carga datos semilla si faltan y verifica conteo por tabla."""
    seed_database()
    engine_name = check_db_connection()

    with get_db() as db:
        counts = {
            "usuarios": db.query(Usuario).count(),
            "pacientes": db.query(Paciente).count(),
            "citas": db.query(Cita).count(),
            "inventario": db.query(Inventario).count(),
            "diagnosticos": db.query(Diagnostico).count(),
            "pagos": db.query(Pago).count(),
        }

    print(f"[OK] Motor de base de datos activo: {engine_name}")
    for table, count in counts.items():
        print(f"  - {table}: {count} registros")

    if engine_name == "sqlite":
        print(
            "[NOTA] DATABASE_URL no esta configurado en .env; "
            "se utilizo SQLite local (consultorio_dental.db)."
        )


if __name__ == "__main__":
    main()
