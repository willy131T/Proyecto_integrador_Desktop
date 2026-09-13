import os
import sys
import subprocess
from pathlib import Path

# Auto-detección y cambio transparente al entorno virtual
base_dir = Path(__file__).resolve().parent
venv_python = base_dir / "venv" / "Scripts" / "python.exe"

if venv_python.exists():
    try:
        is_in_venv = Path(sys.executable).resolve() == venv_python.resolve()
    except Exception:
        is_in_venv = False
    if not is_in_venv:
        print(f"🔄 Activando entorno virtual automáticamente: {venv_python}")
        sys.exit(subprocess.call([str(venv_python)] + sys.argv))

# Asegurar path raíz para importaciones
sys.path.insert(0, str(base_dir))

from config.database import init_db, get_db
from src.models.usuario import Usuario
from src.utils.seed_data import seed_database
from src.ui.app import OdontoApp

def main():
    print("🚀 Iniciando OdontoCloud Desktop...")
    
    # 1. Asegurar sincronización del esquema en base de datos (PostgreSQL / SQLite)
    init_db()

    # 2. Si no existen usuarios, cargar datos semilla iniciales
    with get_db() as db:
        hay_usuarios = db.query(Usuario).first() is not None
        if not hay_usuarios:
            print("🌱 Base de datos vacía. Poblado inicial automático en proceso...")
            seed_database()

    print("✨ Sistema listo. Abriendo interfaz de escritorio...")
    app = OdontoApp()
    app.mainloop()

if __name__ == "__main__":
    main()