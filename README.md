# 🦷 OdontoCloud Desktop — Sistema de Gestión Odontológica Profesional

> **Evolución a Escritorio**: Migración y optimización del proyecto móvil Android hacia una arquitectura de escritorio empresarial en **Python**, con soporte de base de datos **PostgreSQL en la nube (Supabase / Neon)**, control de acceso basado en roles (RBAC), agenda anti-colisiones, emisión de recetas en PDF y control de inventario médico.

---

## 🌟 Características Principales

1. **Multi-Rol con Seguridad Criptográfica**:
   - **Odontólogos / Administradores**: Acceso al tablero de control clínico, agenda general de citas, expedientes con historiales, emisión de recetas en PDF, inventario con alertas de stock bajo y alta de nuevos doctores.
   - **Pacientes**: Autoservicio con bienvenida personalizada, consulta de su próxima cita destacada, historial de tratamientos/recetas y solicitud de nuevas citas.
   - **Contraseñas Seguras**: Hasheadas con algoritmo `bcrypt`.

2. **Base de Datos en la Nube (PostgreSQL)**:
   - Compatible directamente con **Supabase**, **Neon.tech**, **Render** o **AWS RDS**.
   - Incluye respaldo y fallback automático a SQLite local para desarrollo sin conexión o pruebas locales inmediatas.

3. **Agenda Inteligente con Detección de Colisiones**:
   - Algoritmo de validación de horarios en tiempo real: impide que un doctor tenga dos citas agendadas a la misma hora en la misma fecha.

4. **Emisión de Recetas y Expedientes en PDF**:
   - Generación automática de recetas médicas formales con membrete del consultorio, cédula, procedimiento y prescripción farmacológica mediante `ReportLab`.

5. **Control de Inventario Odontológico**:
   - Catálogo clasificado por categorías (*Medicamentos*, *Materiales*, *Desechables*, *Instrumental*).
   - Indicadores visuales de stock crítico (productos con 15 unidades o menos se marcan en rojo).

6. **Interfaz Gráfica Moderna (CustomTkinter)**:
   - Soporte nativo para modo oscuro (*Dark Mode*) y claro (*Light Mode*).
   - Navegación lateral ergonómica y diseño responsivo.

---

## 🚀 Puesta en Marcha Rápida (VS Code / Windows)

### 1. Activar el Entorno Virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Configurar la Base de Datos en la Nube (Opcional)
Abre el archivo `.env` en la raíz. Si deseas conectar a tu PostgreSQL en la nube (ejemplo Supabase o Neon):
```env
DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/postgres?sslmode=require
```
*(Si dejas `DATABASE_URL` vacío, el sistema utiliza automáticamente `consultorio_dental.db` local sin requerir configuración adicional).*

### 3. Ejecutar la Aplicación
```powershell
python main.py
```

### 4. Ejecutar las Pruebas Automatizadas
```powershell
pytest
```
*(Importante: ejecuta `pytest` con `.env` apuntando a SQLite local o vacío, nunca sobre la base PostgreSQL de producción para no insertar registros de prueba).*

---

## ☁️ Producción en la Nube (Live)

- **Backend API (Render):** https://odontocloud-api.onrender.com
- **Documentación Swagger:** https://odontocloud-api.onrender.com/docs
- **Health Check:** https://odontocloud-api.onrender.com/health (`{"status":"ok","database":"connected","engine":"postgresql"}`)
- **Base de Datos Cloud:** Neon PostgreSQL (`odontocloud-db`, región `AWS US East 1`) configurado vía `.env` (nunca se versionan contraseñas ni `DATABASE_URL`).
- **Suite Verificada:** 21 pruebas automatizadas `pytest` (`test_api.py`, `test_services.py` y `test_pagos.py`).
- **Documentación de Usuario:** Consulta [MANUAL_USUARIO.md](MANUAL_USUARIO.md) para guías de Doctor y Paciente.

---

## 🔑 Cuentas Semilla Preconfiguradas (Demo)

| Rol | Usuario | Contraseña | Nombre |
| :--- | :--- | :--- | :--- |
| **Doctor (Admin)** | `admin_doctor` | `12345` | Doctor Admin |
| **Doctora** | `dra_lopez` | `12345` | Dra. López |
| **Doctor** | `dr_martinez` | `12345` | Dr. Martínez |
| **Paciente** | `william_p` | `12345` | William Eduardo Antonio Marcelo |
| **Paciente** | `andres_p` | `12345` | Andrés |
| **Paciente** | `sofi_p` | `12345` | Sofi |

*(La pantalla de inicio de sesión incluye botones de acceso rápido para rellenar automáticamente las credenciales con 1 clic).*

---

## 📦 Compilación a Ejecutable Windows (.exe)

Para compilar la aplicación en un ejecutable autónomo que no requiera tener Python instalado:
```powershell
pyinstaller --noconfirm --onedir --windowed --add-data "config;config" --add-data "src;src" main.py --name "OdontoCloud"
```
El ejecutable se generará dentro de la carpeta `dist/OdontoCloud/OdontoCloud.exe`.