import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Asegurar path raíz para importar src y config
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import init_db, get_db
from src.models.usuario import Usuario
from src.utils.seed_data import seed_database
from api.routes import auth, citas, pacientes, inventario

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización de tablas y seed en el arranque
    init_db()
    with get_db() as db:
        if not db.query(Usuario).first():
            seed_database()
    yield

app = FastAPI(
    title="🦷 OdontoCloud API",
    description="API REST Centralizada para Consultorio Dental • Compatible con Clientes Android (Móvil) y Python (Escritorio).",
    version="2.0.0",
    lifespan=lifespan
)

# Configuración CORS permisiva para conexiones desde emulador Android (10.0.2.2), red local y escritorio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth.router)
app.include_router(citas.router)
app.include_router(pacientes.router)
app.include_router(inventario.router)

@app.get("/", tags=["General"])
def root():
    return {
        "status": "online",
        "sistema": "OdontoCloud API REST",
        "documentacion_swagger": "/docs",
        "documentacion_redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    # Permite escuchar en 0.0.0.0 para que celulares en la misma red WiFi o emuladores puedan conectarse
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)