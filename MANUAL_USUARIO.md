# 📖 Manual de Usuario — OdontoCloud v2.0

Sistema Integral de Gestión Odontológica (Escritorio Python + API Cloud FastAPI + App Móvil Android).

---

## 1. Portal del Odontólogo / Administrador (Escritorio Python)

1. **Inicio de Sesión:** Ejecuta `python main.py` (o `iniciar.bat`) e ingresa con tu usuario y contraseña (`admin_doctor` / `12345` en entorno demo).
2. **Resumen:** Visualiza métricas en tiempo real (total de pacientes, citas pendientes y alertas de stock bajo `<= 15`).
3. **Agenda de Citas:**
   - Filtra citas por **Odontólogo** o **Estado** (`Todos`, `Pendiente`, `Completada`).
   - Agenda nuevas citas con validación automática anti-colisiones.
   - Exporta la agenda completa a **CSV** con el botón `📥 Exportar CSV`.
4. **Expedientes Clínicos:** Consulta alergias, tratamientos activos, registra diagnósticos/recetas y descarga **Recetas Médicas en PDF**.
5. **Inventario:** Administra medicamentos, materiales, desechables e instrumental, con alertas visuales en rojo cuando el stock sea `<= 15`, y exportación a **CSV**.
6. **Pagos y Finanzas:**
   - Registra cobros en **Efectivo**, **Tarjeta** o **Transferencia** (`Pagado` o `Pendiente`).
   - Liquida saldos pendientes con `✓ Liquidar` y genera **Recibos Oficiales en PDF** (`🧾 Recibo PDF`).
7. **BI y Reportes:** Visualiza gráficas de citas por odontólogo, ingresos por método de pago, alertas críticas y exporta reportes CSV.
8. **Equipo Médico:** Da de alta o baja a otros odontólogos (la cuenta principal `admin_doctor` está protegida).

---

## 2. Portal del Paciente (App Móvil Android)

1. **Inicio de Sesión / Registro:** Ingresa con tu cuenta de paciente (`william_p` / `12345` en demo) o regístrate desde la app.
2. **Mi Portal:**
   - Consulta tus **Datos Médicos** (edad y alergias) y tu **Historial Clínico**.
   - Revisa tu **Próxima Cita** sincronizada desde la nube (`https://odontocloud-api.onrender.com`).
   - Consulta tu **Estado de Cuenta y Pagos** (total pagado, saldo pendiente y últimos movimientos).
3. **Agendar Nueva Cita:** Selecciona doctor, fecha, hora y motivo; el sistema evita choques de horario.
4. **Contacto Directo:** Usa el botón **💬 CONTACTAR POR WHATSAPP** para enviar un mensaje directo a la clínica.
