# 🦷 PROMPT DE CONTEXTO MAESTRO: OdontoCloud Desktop & API

Actúa como Desarrollador Full-Stack Senior y colaborador en el proyecto "OdontoCloud Desktop". A continuación tienes todo el contexto técnico, arquitectónico y operativo del repositorio en el que estamos trabajando:

---

## 🎯 1. ¿Qué es este Proyecto?
Es un sistema integral empresarial para consultorios dentales multiplataforma:
1. **Cliente de Escritorio**: Desarrollado en Python con interfaz moderna Dark/Light usando `CustomTkinter`.
2. **Backend Central (API REST)**: Desarrollado en Python con `FastAPI` y `Uvicorn`, con documentación Swagger automática en `/docs`.
3. **Cliente Móvil (Android)**: App nativa en Java que consume esta misma API central mediante `Retrofit 2`.
4. **Base de Datos**: PostgreSQL en la nube (Supabase / Neon) gestionado con `SQLAlchemy 2.0`, con fallback automático a SQLite local (`consultorio_dental.db`) para desarrollo offline.

---

## 🏛️ 2. Arquitectura de Carpetas (Clean Architecture)
El proyecto está desacoplado bajo principios de Arquitectura Limpia:

- `config/`:
  - `settings.py`: Variables de entorno, paths y paleta de colores del tema.
  - `database.py`: Engine de SQLAlchemy, pooler de conexiones y SessionLocal.
- `src/models/`: Modelos ORM (tablas de PostgreSQL): `Usuario`, `Paciente`, `Cita`, `Inventario`, `Diagnostico`.
- `src/schemas/`: Esquemas de validación de datos con `Pydantic v2`.
- `src/services/`: Lógica de negocio pura (CERO interfaz aquí):
  - `auth_service.py`: Login, registro, hashing `bcrypt` y gestión de doctores.
  - `cita_service.py`: Agendamiento con prevención estricta de colisiones de horario.
  - `paciente_service.py`: Búsqueda de pacientes y expedientes clínicos.
  - `inventario_service.py`: Control de insumos y alertas de stock bajo (<= 15).
  - `diagnostico_service.py`: Procedimientos médicos y actualización de tratamientos.
  - `pdf_service.py`: Generación de recetas oficiales en PDF con `ReportLab`.
- `src/ui/`: Capa visual de escritorio (`CustomTkinter`):
  - `app.py`: Enrutador de ventanas y gestor de sesión.
  - `views/`: `login_view.py`, `registro_view.py`, `doctor_dashboard.py`, `paciente_dashboard.py`.
  - `components/`: `sidebar.py`, modales y tarjetas estadísticas.
- `api/`:
  - `main.py`: Entrada del servidor FastAPI con middlewares CORS habilitados.
  - `routes/`: Endpoints REST (`auth.py`, `citas.py`, `pacientes.py`, `inventario.py`).
- `tests/`: Pruebas automatizadas con `pytest` (`test_services.py`, `test_api.py`).
- `iniciar.bat` / `iniciar_servidor.bat`: Lanzadores rápidos de Windows.

---

## 👥 3. Roles del Sistema (RBAC)
- **Rol `dentista` (Doctor / Dueño)**:
  - Gestiona citas, expedientes, diagnósticos e inventario.
  - Puede dar de alta a nuevos colegas doctores o darles de baja (el sistema protege la cuenta del Dueño principal `admin_doctor` y previene auto-eliminaciones).
- **Rol `paciente`**:
  - Consulta su próxima cita destacada, historial de recetas y auto-agenda citas con su doctor favorito validando disponibilidad de horario.

---

## 🚨 4. Reglas de Desarrollo Obligatorias
1. **Regla de Git**: La rama `main` está protegida. NUNCA hagas push directo a `main`. Todo cambio se realiza en una rama propia (`git checkout -b feature/nombre-tarea`) y se sube mediante Pull Request.
2. **Separación de Capas**: NUNCA coloques consultas SQL ni lógica de negocio dentro de los archivos de la interfaz gráfica (`src/ui/`). Toda regla de negocio debe ir en `src/services/` y ser consumida por la UI o por la API.
3. **Manejo de Secretos**: NUNCA escribas contraseñas ni URLs de bases de datos hardcodeadas en el código. Se leen siempre desde `.env`.
4. **Verificación**: Antes de solicitar un Pull Request, ejecuta siempre la suite de pruebas unitarias con `pytest` en la terminal (con `.env` apuntando a SQLite local). Todas las 21 pruebas deben pasar en verde.

---

## 🛠️ 5. Comandos de Referencia Rápida y Producción en la Nube
- Activar entorno: `.\venv\Scripts\Activate.ps1`
- Ejecutar App de Escritorio: `python main.py`
- Ejecutar Servidor API: `python -m uvicorn api.main:app --reload` (Documentación en `http://127.0.0.1:8000/docs`)
- Ejecutar Pruebas: `pytest` *(15 pruebas en verde; ejecutar siempre con `.env` apuntando a SQLite local, nunca a Neon producción)*

### Producción en la Nube (Live)
- **Backend FastAPI (Render):** https://odontocloud-api.onrender.com
- **Swagger Docs:** https://odontocloud-api.onrender.com/docs
- **Health Check (`/health`):** `{"status":"ok","database":"connected","engine":"postgresql"}`
- **Base de Datos Cloud:** Neon PostgreSQL (`odontocloud-db`, región `AWS US East 1`), configurada en `.env` local y en Render (nunca expongas `DATABASE_URL` en commits).

Ayúdame a [DESCRIBE TU TAREA AQUÍ, EJ: agregar un nuevo reporte en PDF / conectar un nuevo endpoint / diseñar una vista] respetando estrictamente esta arquitectura.