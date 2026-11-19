import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL

logger = logging.getLogger(__name__)

engine_kwargs = {
    "pool_pre_ping": True,
    "echo": False,
}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Reciclar conexiones antes de que el compute serverless (Neon/Supabase) las cierre por inactividad
    engine_kwargs["pool_recycle"] = 300

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error en sesión de base de datos: {e}")
        raise
    finally:
        db.close()

def check_db_connection() -> str:
    """Verifica conectividad real a la BD y retorna el motor activo ('sqlite' o 'postgresql')."""
    with get_db() as db:
        db.execute(text("SELECT 1"))
    return "sqlite" if DATABASE_URL.startswith("sqlite") else "postgresql"

def init_db():
    import src.models
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas sincronizadas correctamente en la base de datos.")