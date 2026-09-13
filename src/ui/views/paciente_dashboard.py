from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from config.settings import THEME
from src.services.cita_service import CitaService
from src.services.diagnostico_service import DiagnosticoService
from src.services.paciente_service import PacienteService
from src.services.auth_service import AuthService

class PacienteDashboard(ctk.CTkFrame):
    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color=("white", "#0F172A"))
        self.usuario = usuario

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.show_view("dashboard")

    def show_view(self, view_id):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_id in ["dashboard", "mis_citas"]:
            self._render_portal()
        elif view_id == "agendar":
            self._modal_agendar_cita()
            self._render_portal()

    def _render_portal(self):
        # 1. Cabecera del Paciente
        pac_info = PacienteService.obtener_paciente_por_nombre(self.usuario.get("nombre"))
        edad = pac_info["edad"] if pac_info else self.usuario.get("edad", 0)
        alergias = pac_info["alergias"] if pac_info else self.usuario.get("alergias", "Ninguna")

        header = ctk.CTkFrame(self.content_frame, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12, border_width=1, border_color=("#E2E8F0", "#334155"))
        header.pack(fill="x", pady=(0, 20))

        top_row = ctk.CTkFrame(header, fg_color="transparent")
        top_row.pack(fill="x", padx=20, pady=(15, 6))

        lbl_saludo = ctk.CTkLabel(
            top_row,
            text=f"👋 ¡Hola, {self.usuario.get('nombre')}!",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["primary"]
        )
        lbl_saludo.pack(side="left")

        btn_agendar = ctk.CTkButton(
            top_row,
            text="➕ Agendar Nueva Cita",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=THEME["primary"],
            command=self._modal_agendar_cita
        )
        btn_agendar.pack(side="right")

        info_badges = ctk.CTkFrame(header, fg_color="transparent")
        info_badges.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(info_badges, text=f"🎂 Edad: {edad} años", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 15))

        alergia_color = THEME["danger"] if alergias != "Ninguna" else THEME["success"]
        ctk.CTkLabel(info_badges, text=f"⚠️ Alergias: {alergias}", font=ctk.CTkFont(size=12, weight="bold"), text_color=alergia_color).pack(side="left")

        # 2. Tarjeta Destacada de Próxima Cita
        proxima = CitaService.obtener_proxima_cita_paciente(self.usuario.get("nombre"))
        cita_card = ctk.CTkFrame(self.content_frame, fg_color=("#E0F2FE", "#082F49"), corner_radius=12, border_width=1, border_color=("#BAE6FD", "#0369A1"))
        cita_card.pack(fill="x", pady=(0, 20))

        if proxima:
            ctk.CTkLabel(cita_card, text="📅 TU PRÓXIMA CITA ODONTOLÓGICA", font=ctk.CTkFont(size=11, weight="bold"), text_color=THEME["primary"]).pack(anchor="w", padx=16, pady=(12, 2))
            ctk.CTkLabel(cita_card, text=f"Fecha: {proxima['fecha']} a las {proxima['hora']} hrs", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=2)
            ctk.CTkLabel(cita_card, text=f"👨‍⚕️ Atiende: {proxima['doctor']}  •  🦷 Motivo: {proxima['motivo']}", font=ctk.CTkFont(size=12), text_color="#475569").pack(anchor="w", padx=16, pady=(0, 12))
        else:
            ctk.CTkLabel(cita_card, text="📅 Estado de Citas", font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748B").pack(anchor="w", padx=16, pady=(12, 2))
            ctk.CTkLabel(cita_card, text="No tienes citas agendadas actualmente.", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=16, pady=(2, 12))

        # 3. Dos Columnas: Mis Tratamientos / Diagnósticos vs Historial de Citas
        grid_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        # Columna Izquierda: Tratamientos y Diagnósticos
        left_col = ctk.CTkFrame(grid_frame, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_col, text="🩺 Diagnósticos y Tratamientos", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))

        scroll_diag = ctk.CTkScrollableFrame(left_col, fg_color="transparent", height=220)
        scroll_diag.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        diagnosticos = DiagnosticoService.obtener_diagnosticos_por_paciente(self.usuario.get("nombre"))
        if not diagnosticos:
            ctk.CTkLabel(scroll_diag, text="Sin diagnósticos registrados aún.").pack(pady=20)
        else:
            for d in diagnosticos:
                d_card = ctk.CTkFrame(scroll_diag, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
                d_card.pack(fill="x", pady=4)

                ctk.CTkLabel(d_card, text=f"🗓️ {d['fecha']} • {d['cita_info']}", font=ctk.CTkFont(size=11, weight="bold"), text_color=THEME["primary"]).pack(anchor="w", padx=10, pady=(8, 2))
                ctk.CTkLabel(d_card, text=f"🦷 {d['procedimiento']}", font=ctk.CTkFont(size=11), justify="left").pack(anchor="w", padx=10, pady=2)
                if d['medicamentos'] and d['medicamentos'] != "Ninguno":
                    ctk.CTkLabel(d_card, text=f"💊 Receta: {d['medicamentos']}", font=ctk.CTkFont(size=11), text_color="#10B981", justify="left").pack(anchor="w", padx=10, pady=(2, 8))

        # Columna Derecha: Todas Mis Citas
        right_col = ctk.CTkFrame(grid_frame, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12)
        right_col.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(right_col, text="📋 Historial de Citas", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))

        scroll_citas = ctk.CTkScrollableFrame(right_col, fg_color="transparent", height=220)
        scroll_citas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        mis_citas = CitaService.obtener_citas_por_paciente(self.usuario.get("nombre"))
        if not mis_citas:
            ctk.CTkLabel(scroll_citas, text="No tienes citas en el historial.").pack(pady=20)
        else:
            for c in mis_citas:
                c_card = ctk.CTkFrame(scroll_citas, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
                c_card.pack(fill="x", pady=4)

                st_color = "#10B981" if c["estado"] == "Completada" else "#0284C7"
                ctk.CTkLabel(c_card, text=f"🗓️ {c['fecha']} a las {c['hora']}", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=10, pady=(6, 2))
                ctk.CTkLabel(c_card, text=f"👨‍⚕️ {c['doctor']} • {c['motivo']}", font=ctk.CTkFont(size=11), text_color="#64748B").pack(anchor="w", padx=10, pady=2)
                ctk.CTkLabel(c_card, text=f"Estado: {c['estado']}", font=ctk.CTkFont(size=10, weight="bold"), text_color=st_color).pack(anchor="w", padx=10, pady=(0, 6))

    def _modal_agendar_cita(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Agendar Cita Odontológica")
        modal.geometry("420x440")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Agendar Cita", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 12))

        ctk.CTkLabel(modal, text="Odontólogo Preferido:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        doctores = AuthService.obtener_doctores()
        combo_doctor = ctk.CTkComboBox(modal, values=doctores, width=360)
        combo_doctor.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Fecha (DD/MM/YYYY):", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        entry_fecha = ctk.CTkEntry(modal, width=360, placeholder_text="ej: 15/09/2026")
        entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_fecha.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Hora (HH:MM):", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        entry_hora = ctk.CTkEntry(modal, width=360, placeholder_text="ej: 11:30")
        entry_hora.insert(0, "11:00")
        entry_hora.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Motivo de la Cita:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        motivos = ["Limpieza dental (Profilaxis)", "Ortodoncia (Ajuste / Revision)", "Extracción dental", "Dolor agudo / Urgencia", "Revisión general", "Resina / Calce", "Otro..."]
        combo_motivo = ctk.CTkComboBox(modal, values=motivos, width=360)
        combo_motivo.pack(pady=(0, 15))

        lbl_status = ctk.CTkLabel(modal, text="", font=ctk.CTkFont(size=11), text_color=THEME["danger"])
        lbl_status.pack(pady=2)

        def _guardar():
            doc = combo_doctor.get().strip()
            fec = entry_fecha.get().strip()
            hor = entry_hora.get().strip()
            mot = combo_motivo.get().strip()

            if not doc or not fec or not hor or not mot:
                lbl_status.configure(text="Todos los campos son obligatorios.")
                return

            # Comprobar disponibilidad de horario con el doctor
            if CitaService.verificar_disponibilidad(doc, fec, hor):
                lbl_status.configure(text=f"❌ El {doc} ya tiene cita el {fec} a las {hor}. Elige otra hora.")
                return

            CitaService.agendar_cita(self.usuario.get("nombre"), doc, fec, hor, mot)
            modal.destroy()
            messagebox.showinfo("Cita Agendada", "¡Tu cita ha sido agendada con éxito!")
            self._render_portal()

        ctk.CTkButton(modal, text="Confirmar Cita", fg_color=THEME["primary"], height=38, command=_guardar).pack(pady=10)