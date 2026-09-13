import os
import subprocess
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from config.settings import THEME
from src.services.cita_service import CitaService
from src.services.paciente_service import PacienteService
from src.services.inventario_service import InventarioService
from src.services.diagnostico_service import DiagnosticoService
from src.services.pdf_service import PDFService
from src.services.auth_service import AuthService

class DoctorDashboard(ctk.CTkFrame):
    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color=("white", "#0F172A"))
        self.usuario = usuario

        # Contenedor dinámico de contenido
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.show_view("dashboard")

    def show_view(self, view_id):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_id == "dashboard":
            self._render_dashboard()
        elif view_id == "citas":
            self._render_citas()
        elif view_id == "pacientes":
            self._render_pacientes()
        elif view_id == "inventario":
            self._render_inventario()
        elif view_id == "nuevo_doctor":
            self._render_nuevo_doctor_modal()

    # ==========================================
    # 1. VISTA DASHBOARD / RESUMEN
    # ==========================================
    def _render_dashboard(self):
        # Título
        lbl = ctk.CTkLabel(
            self.content_frame,
            text=f"Bienvenido/a, {self.usuario.get('nombre')}",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl.pack(anchor="w", pady=(0, 2))

        lbl_sub = ctk.CTkLabel(
            self.content_frame,
            text="Panel de Control General • Consultorio Odontológico",
            font=ctk.CTkFont(size=12),
            text_color="#64748B"
        )
        lbl_sub.pack(anchor="w", pady=(0, 20))

        # Tarjetas de Métricas
        pacientes = PacienteService.obtener_pacientes()
        citas = CitaService.obtener_todas_las_citas()
        citas_pendientes = [c for c in citas if c["estado"] == "Pendiente"]
        alertas_inv = InventarioService.obtener_alertas_stock_bajo(15)

        cards_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        metrics = [
            ("👥 Total Pacientes", str(len(pacientes)), "#0284C7", 0),
            ("📅 Citas Pendientes", str(len(citas_pendientes)), "#0D9488", 1),
            ("⚠️ Stock Bajo (<15)", str(len(alertas_inv)), "#EF4444" if alertas_inv else "#10B981", 2),
        ]

        for title, val, color, col in metrics:
            card = ctk.CTkFrame(cards_frame, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12, border_width=1, border_color=("#E2E8F0", "#334155"))
            card.grid(row=0, column=col, padx=8, sticky="ew")

            lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#64748B")
            lbl_t.pack(anchor="w", padx=16, pady=(14, 2))

            lbl_v = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=28, weight="bold"), text_color=color)
            lbl_v.pack(anchor="w", padx=16, pady=(0, 14))

        # Sección: Próximas Citas
        lbl_citas = ctk.CTkLabel(self.content_frame, text="📋 Citas Recientes en Agenda", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_citas.pack(anchor="w", pady=(10, 10))

        scroll = ctk.CTkScrollableFrame(self.content_frame, height=280, fg_color=("#F8FAFC", "#1E293B"))
        scroll.pack(fill="both", expand=True)

        if not citas:
            ctk.CTkLabel(scroll, text="No hay citas registradas.").pack(pady=20)
        else:
            for c in citas[:8]:
                row = ctk.CTkFrame(scroll, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
                row.pack(fill="x", padx=6, pady=4)

                ctk.CTkLabel(row, text=f"🗓️ {c['fecha']} {c['hora']}", font=ctk.CTkFont(size=12, weight="bold"), width=150, anchor="w").pack(side="left", padx=12, pady=10)
                ctk.CTkLabel(row, text=f"👤 {c['paciente']}", font=ctk.CTkFont(size=12), width=180, anchor="w").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=f"👨‍⚕️ {c['doctor']}", font=ctk.CTkFont(size=12), text_color="#64748B", width=140, anchor="w").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=f"🦷 {c['motivo']}", font=ctk.CTkFont(size=11), anchor="w").pack(side="left", padx=8, fill="x", expand=True)

                badge_color = "#10B981" if c['estado'] == "Completada" else "#0284C7"
                ctk.CTkLabel(row, text=c['estado'], font=ctk.CTkFont(size=10, weight="bold"), text_color=badge_color, width=80).pack(side="right", padx=12)

    # ==========================================
    # 2. VISTA DE CITAS & AGENDA
    # ==========================================
    def _render_citas(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        lbl = ctk.CTkLabel(header, text="Agenda Odontológica", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(side="left")

        btn_nueva = ctk.CTkButton(
            header,
            text="➕ Agendar Nueva Cita",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=THEME["primary"],
            command=self._modal_agendar_cita
        )
        btn_nueva.pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color=("#F8FAFC", "#1E293B"))
        scroll.pack(fill="both", expand=True)

        citas = CitaService.obtener_todas_las_citas()
        if not citas:
            ctk.CTkLabel(scroll, text="No hay citas programadas.").pack(pady=40)
            return

        for c in citas:
            row = ctk.CTkFrame(scroll, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
            row.pack(fill="x", padx=6, pady=4)

            ctk.CTkLabel(row, text=f"📅 {c['fecha']} [{c['hora']}]", font=ctk.CTkFont(size=12, weight="bold"), width=150, anchor="w").pack(side="left", padx=12, pady=12)
            ctk.CTkLabel(row, text=f"👤 {c['paciente']}", font=ctk.CTkFont(size=12), width=180, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"👨‍⚕️ {c['doctor']}", font=ctk.CTkFont(size=12), text_color="#64748B", width=140, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"🦷 {c['motivo']}", font=ctk.CTkFont(size=11), anchor="w").pack(side="left", padx=8, fill="x", expand=True)

            # Botón Completar
            if c['estado'] == "Pendiente":
                btn_comp = ctk.CTkButton(
                    row,
                    text="✓ Completar",
                    width=80,
                    height=28,
                    font=ctk.CTkFont(size=10),
                    fg_color="#10B981",
                    command=lambda cid=c['id']: self._marcar_completada(cid)
                )
                btn_comp.pack(side="right", padx=6)

            # Botón Cancelar/Eliminar
            btn_del = ctk.CTkButton(
                row,
                text="✕ Cancelar",
                width=75,
                height=28,
                font=ctk.CTkFont(size=10),
                fg_color="#EF4444",
                command=lambda cid=c['id']: self._eliminar_cita(cid)
            )
            btn_del.pack(side="right", padx=6)

    def _marcar_completada(self, id_cita):
        CitaService.cambiar_estado_cita(id_cita, "Completada")
        self.show_view("citas")

    def _eliminar_cita(self, id_cita):
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar o cancelar esta cita?"):
            CitaService.eliminar_cita(id_cita)
            self.show_view("citas")

    def _modal_agendar_cita(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Agendar Cita Odontológica")
        modal.geometry("450x480")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Agendar Nueva Cita", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 15))

        pacientes = [p["nombre"] for p in PacienteService.obtener_pacientes()]
        if not pacientes:
            pacientes = ["Paciente General"]

        ctk.CTkLabel(modal, text="Selecciona el Paciente:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        combo_paciente = ctk.CTkComboBox(modal, values=pacientes, width=380)
        combo_paciente.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Odontólogo Tratante:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        doctores = AuthService.obtener_doctores()
        combo_doctor = ctk.CTkComboBox(modal, values=doctores, width=380)
        combo_doctor.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Fecha (DD/MM/YYYY):", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        entry_fecha = ctk.CTkEntry(modal, width=380, placeholder_text="ej: 25/08/2026")
        entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_fecha.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Hora (HH:MM):", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        entry_hora = ctk.CTkEntry(modal, width=380, placeholder_text="ej: 10:30")
        entry_hora.insert(0, "10:00")
        entry_hora.pack(pady=(0, 8))

        ctk.CTkLabel(modal, text="Motivo de Consulta:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        motivos = ["Limpieza dental (Profilaxis)", "Ortodoncia (Ajuste / Revision)", "Extracción dental", "Dolor agudo / Urgencia", "Revisión general", "Resina / Calce"]
        combo_motivo = ctk.CTkComboBox(modal, values=motivos, width=380)
        combo_motivo.pack(pady=(0, 15))

        lbl_status = ctk.CTkLabel(modal, text="", font=ctk.CTkFont(size=11), text_color=THEME["danger"])
        lbl_status.pack(pady=2)

        def _guardar():
            pac = combo_paciente.get().strip()
            doc = combo_doctor.get().strip()
            fec = entry_fecha.get().strip()
            hor = entry_hora.get().strip()
            mot = combo_motivo.get().strip()

            if not pac or not doc or not fec or not hor or not mot:
                lbl_status.configure(text="Todos los campos son obligatorios.")
                return

            if CitaService.verificar_disponibilidad(doc, fec, hor):
                lbl_status.configure(text=f"❌ El {doc} ya tiene cita el {fec} a las {hor}.")
                return

            CitaService.agendar_cita(pac, doc, fec, hor, mot)
            modal.destroy()
            self.show_view("citas")

        ctk.CTkButton(modal, text="Confirmar y Guardar Cita", fg_color=THEME["primary"], height=38, command=_guardar).pack(pady=10)

    # ==========================================
    # 3. VISTA DE PACIENTES Y EXPEDIENTES
    # ==========================================
    def _render_pacientes(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        lbl = ctk.CTkLabel(header, text="Expedientes Clínicos", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(side="left")

        # Barra de búsqueda
        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.pack(side="right")

        entry_buscar = ctk.CTkEntry(search_frame, width=220, placeholder_text="Buscar por nombre...")
        entry_buscar.pack(side="left", padx=6)

        btn_buscar = ctk.CTkButton(
            search_frame,
            text="🔍 Buscar",
            width=80,
            command=lambda: self._buscar_pacientes(entry_buscar.get())
        )
        btn_buscar.pack(side="left")

        # Contenedor dividido: Lista a la izquierda, Detalle a la derecha
        self.split_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.split_frame.pack(fill="both", expand=True)
        self.split_frame.grid_columnconfigure(0, weight=2)
        self.split_frame.grid_columnconfigure(1, weight=3)

        self.list_frame = ctk.CTkScrollableFrame(self.split_frame, fg_color=("#F8FAFC", "#1E293B"))
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.detail_frame = ctk.CTkFrame(self.split_frame, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12)
        self.detail_frame.grid(row=0, column=1, sticky="nsew")

        self._cargar_lista_pacientes()

    def _buscar_pacientes(self, query):
        self._cargar_lista_pacientes(filtro=query)

    def _cargar_lista_pacientes(self, filtro=None):
        for w in self.list_frame.winfo_children():
            w.destroy()

        pacientes = PacienteService.obtener_pacientes(filtro)
        if not pacientes:
            ctk.CTkLabel(self.list_frame, text="No se encontraron pacientes.").pack(pady=30)
            return

        for p in pacientes:
            card = ctk.CTkFrame(self.list_frame, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8, cursor="hand2")
            card.pack(fill="x", padx=4, pady=4)
            card.bind("<Button-1>", lambda e, pac=p: self._mostrar_detalle_paciente(pac))

            lbl_n = ctk.CTkLabel(card, text=f"👤 {p['nombre']}", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
            lbl_n.pack(anchor="w", padx=12, pady=(8, 2))
            lbl_n.bind("<Button-1>", lambda e, pac=p: self._mostrar_detalle_paciente(pac))

            info_text = f"🎂 {p['edad']} años • Alergias: {p['alergias']}"
            lbl_i = ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(size=11), text_color="#64748B", anchor="w")
            lbl_i.pack(anchor="w", padx=12, pady=(0, 8))
            lbl_i.bind("<Button-1>", lambda e, pac=p: self._mostrar_detalle_paciente(pac))

        # Mostrar el primero por defecto
        if pacientes:
            self._mostrar_detalle_paciente(pacientes[0])

    def _mostrar_detalle_paciente(self, pac):
        for w in self.detail_frame.winfo_children():
            w.destroy()

        scroll_detail = ctk.CTkScrollableFrame(self.detail_frame, fg_color="transparent")
        scroll_detail.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(scroll_detail, text=pac["nombre"], font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(scroll_detail, text=f"🎂 Edad: {pac['edad']} años  •  📞 Tel: {pac['telefono']}  •  ✉️ {pac['correo']}", font=ctk.CTkFont(size=12), text_color="#64748B").pack(anchor="w", pady=(0, 10))

        # Alergias
        alergias_box = ctk.CTkFrame(scroll_detail, fg_color=("#FEF2F2", "#450A0A") if pac["alergias"] != "Ninguna" else ("#F0FDF4", "#052E16"), corner_radius=8)
        alergias_box.pack(fill="x", pady=6)
        ctk.CTkLabel(alergias_box, text=f"⚠️ Alergias Registradas: {pac['alergias']}", font=ctk.CTkFont(size=11, weight="bold"), text_color=THEME["danger"] if pac["alergias"] != "Ninguna" else THEME["success"]).pack(padx=10, pady=8, anchor="w")

        # Tratamiento Actual
        ctk.CTkLabel(scroll_detail, text="🦷 Tratamiento Activo:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10, 2))
        trat_card = ctk.CTkFrame(scroll_detail, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
        trat_card.pack(fill="x", pady=4)
        ctk.CTkLabel(trat_card, text=pac["tratamiento"], font=ctk.CTkFont(size=11), justify="left", anchor="w").pack(padx=12, pady=10, fill="x")

        # Botones de Acción
        actions_frame = ctk.CTkFrame(scroll_detail, fg_color="transparent")
        actions_frame.pack(fill="x", pady=15)

        ctk.CTkButton(
            actions_frame,
            text="📝 Nuevo Diagnóstico / Receta",
            fg_color=THEME["secondary"],
            command=lambda: self._modal_nuevo_diagnostico(pac)
        ).pack(side="left", padx=4)

        # Historial de Diagnósticos Registrados
        ctk.CTkLabel(scroll_detail, text="📜 Historial de Consultas y Procedimientos:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(15, 6))

        diagnosticos = DiagnosticoService.obtener_diagnosticos_por_paciente(pac["nombre"])
        if not diagnosticos:
            ctk.CTkLabel(scroll_detail, text="No hay diagnósticos previos registrados.", font=ctk.CTkFont(size=11), text_color="#64748B").pack(anchor="w", pady=6)
        else:
            for d in diagnosticos:
                d_card = ctk.CTkFrame(scroll_detail, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
                d_card.pack(fill="x", pady=4)

                header_d = ctk.CTkFrame(d_card, fg_color="transparent")
                header_d.pack(fill="x", padx=10, pady=(8, 2))

                ctk.CTkLabel(header_d, text=f"🗓️ Fecha: {d['fecha']} • {d['cita_info']}", font=ctk.CTkFont(size=11, weight="bold"), text_color=THEME["primary"]).pack(side="left")

                # Botón Exportar PDF de esta consulta
                btn_pdf = ctk.CTkButton(
                    header_d,
                    text="📄 Descargar PDF",
                    width=90,
                    height=24,
                    font=ctk.CTkFont(size=10),
                    fg_color="#0284C7",
                    command=lambda diag=d, pnom=pac["nombre"]: self._generar_pdf_receta(pnom, diag)
                )
                btn_pdf.pack(side="right")

                ctk.CTkLabel(d_card, text=f"🩺 Procedimiento: {d['procedimiento']}", font=ctk.CTkFont(size=11), justify="left", anchor="w").pack(anchor="w", padx=10, pady=2)
                if d['medicamentos'] and d['medicamentos'] != "Ninguno":
                    ctk.CTkLabel(d_card, text=f"💊 Receta / Farmacia: {d['medicamentos']}", font=ctk.CTkFont(size=11), text_color="#10B981", justify="left", anchor="w").pack(anchor="w", padx=10, pady=(2, 8))

    def _generar_pdf_receta(self, paciente_nombre, diag):
        try:
            pdf_path = PDFService.generar_receta_medica(
                paciente_nombre=paciente_nombre,
                doctor_nombre=self.usuario.get("nombre", "Dr. Odontólogo"),
                procedimiento=diag["procedimiento"],
                medicamentos=diag["medicamentos"],
                fecha=diag["fecha"]
            )
            messagebox.showinfo("PDF Generado", f"Receta médica generada con éxito:\n\n{pdf_path}")
            # Abrir automáticamente el PDF en el visor predeterminado de Windows
            if os.name == 'nt':
                os.startfile(pdf_path)
        except Exception as e:
            messagebox.showerror("Error al generar PDF", str(e))

    def _modal_nuevo_diagnostico(self, pac):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Diagnóstico Clínico - {pac['nombre']}")
        modal.geometry("480x480")
        modal.grab_set()

        ctk.CTkLabel(modal, text=f"Registrar Procedimiento: {pac['nombre']}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(18, 12))

        # Citas del paciente para vincular
        citas_p = CitaService.obtener_citas_por_paciente(pac["nombre"])
        citas_options = [f"Cita: {c['fecha']} [{c['hora']}] - {c['motivo']}" for c in citas_p]
        if not citas_options:
            citas_options = ["Consulta Directa / Sin Cita Previa"]

        ctk.CTkLabel(modal, text="Vincular a Cita:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        combo_citas = ctk.CTkComboBox(modal, values=citas_options, width=420)
        combo_citas.pack(pady=(0, 10))

        ctk.CTkLabel(modal, text="Procedimiento Odontológico Realizado:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        txt_proc = ctk.CTkTextbox(modal, width=420, height=100)
        txt_proc.pack(pady=(0, 10))

        ctk.CTkLabel(modal, text="Prescripción Farmacológica (Medicamentos y Dosis):", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=30, pady=(4, 2))
        txt_meds = ctk.CTkTextbox(modal, width=420, height=80)
        txt_meds.pack(pady=(0, 15))

        def _guardar_diag():
            proc = txt_proc.get("1.0", "end").strip()
            meds = txt_meds.get("1.0", "end").strip()
            cita_info = combo_citas.get()

            if not proc:
                messagebox.showwarning("Atención", "El procedimiento es obligatorio.")
                return

            DiagnosticoService.insertar_diagnostico(
                nombre_paciente=pac["nombre"],
                cita_info=cita_info,
                procedimiento=proc,
                medicamentos=meds
            )

            modal.destroy()
            messagebox.showinfo("Éxito", "Diagnóstico registrado y tratamiento actualizado.")
            self.show_view("pacientes")

        ctk.CTkButton(modal, text="Guardar Diagnóstico y Actualizar Ficha", fg_color=THEME["primary"], height=38, command=_guardar_diag).pack(pady=8)

    # ==========================================
    # 4. VISTA DE INVENTARIO
    # ==========================================
    def _render_inventario(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        lbl = ctk.CTkLabel(header, text="Inventario de Insumos y Medicamentos", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(side="left")

        btn_nuevo = ctk.CTkButton(
            header,
            text="➕ Registrar Insumo",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=THEME["primary"],
            command=self._modal_nuevo_material
        )
        btn_nuevo.pack(side="right")

        # Filtros de Categoría y Búsqueda
        filter_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_bar.pack(fill="x", pady=(0, 12))

        categorias = ["Todas", "Medicamentos", "Materiales", "Desechables", "Instrumental"]
        self.combo_cat = ctk.CTkComboBox(
            filter_bar,
            values=categorias,
            width=160,
            command=lambda val: self._filtrar_inventario()
        )
        self.combo_cat.set("Todas")
        self.combo_cat.pack(side="left", padx=(0, 10))

        self.entry_inv_search = ctk.CTkEntry(filter_bar, width=250, placeholder_text="Buscar insumo...")
        self.entry_inv_search.pack(side="left", padx=(0, 8))

        btn_filtrar = ctk.CTkButton(filter_bar, text="Filtrar", width=70, command=self._filtrar_inventario)
        btn_filtrar.pack(side="left")

        self.inv_scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color=("#F8FAFC", "#1E293B"))
        self.inv_scroll.pack(fill="both", expand=True)

        self._cargar_items_inventario()

    def _filtrar_inventario(self):
        cat = self.combo_cat.get()
        query = self.entry_inv_search.get().strip()
        self._cargar_items_inventario(categoria=cat, busqueda=query)

    def _cargar_items_inventario(self, categoria="Todas", busqueda=""):
        for w in self.inv_scroll.winfo_children():
            w.destroy()

        materiales = InventarioService.obtener_inventario(categoria, busqueda)
        if not materiales:
            ctk.CTkLabel(self.inv_scroll, text="No hay insumos que coincidan con la búsqueda.").pack(pady=30)
            return

        for m in materiales:
            row = ctk.CTkFrame(self.inv_scroll, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
            row.pack(fill="x", padx=4, pady=3)

            # Indicador de stock
            es_critico = m['cantidad'] <= 15
            color_cant = "#EF4444" if es_critico else "#10B981"
            tag_text = " ⚠️ STOCK BAJO" if es_critico else ""

            ctk.CTkLabel(row, text=f"📦 {m['nombre']}", font=ctk.CTkFont(size=12, weight="bold"), width=280, anchor="w").pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(row, text=f"🏷️ {m['categoria']}", font=ctk.CTkFont(size=11), text_color="#64748B", width=140, anchor="w").pack(side="left", padx=8)

            cant_label = ctk.CTkLabel(row, text=f"Cantidad: {m['cantidad']}{tag_text}", font=ctk.CTkFont(size=12, weight="bold"), text_color=color_cant, width=180, anchor="w")
            cant_label.pack(side="left", padx=8)

            # Botones Editar y Eliminar
            btn_edit = ctk.CTkButton(
                row,
                text="✏️ Ajustar",
                width=75,
                height=26,
                font=ctk.CTkFont(size=10),
                fg_color="#0284C7",
                command=lambda mat=m: self._modal_editar_material(mat)
            )
            btn_edit.pack(side="right", padx=6)

            btn_del = ctk.CTkButton(
                row,
                text="🗑️",
                width=35,
                height=26,
                font=ctk.CTkFont(size=10),
                fg_color="#EF4444",
                command=lambda mid=m['id'], mnom=m['nombre']: self._eliminar_material(mid, mnom)
            )
            btn_del.pack(side="right", padx=4)

    def _eliminar_material(self, id_mat, nombre):
        if messagebox.askyesno("Eliminar Insumo", f"¿Estás seguro de eliminar '{nombre}' del inventario?"):
            InventarioService.eliminar_material(id_mat)
            self._filtrar_inventario()

    def _modal_nuevo_material(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Registrar Insumo")
        modal.geometry("380x360")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Nuevo Insumo / Material", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        entry_nombre = ctk.CTkEntry(modal, width=300, placeholder_text="Nombre del material o medicina")
        entry_nombre.pack(pady=8)

        entry_cant = ctk.CTkEntry(modal, width=300, placeholder_text="Cantidad en stock")
        entry_cant.pack(pady=8)

        combo_cat = ctk.CTkComboBox(modal, values=["Materiales", "Medicamentos", "Desechables", "Instrumental"], width=300)
        combo_cat.pack(pady=8)

        def _guardar():
            nom = entry_nombre.get().strip()
            cant_str = entry_cant.get().strip()
            cat = combo_cat.get()
            if not nom or not cant_str:
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                return
            try:
                cant = int(cant_str)
            except ValueError:
                messagebox.showwarning("Atención", "La cantidad debe ser numérica.")
                return

            InventarioService.insertar_material(nom, cant, cat)
            modal.destroy()
            self._filtrar_inventario()

        ctk.CTkButton(modal, text="Guardar Insumo", fg_color=THEME["primary"], height=36, command=_guardar).pack(pady=15)

    def _modal_editar_material(self, mat):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Editar {mat['nombre']}")
        modal.geometry("380x360")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Editar Insumo", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        entry_nombre = ctk.CTkEntry(modal, width=300)
        entry_nombre.insert(0, mat["nombre"])
        entry_nombre.pack(pady=8)

        entry_cant = ctk.CTkEntry(modal, width=300)
        entry_cant.insert(0, str(mat["cantidad"]))
        entry_cant.pack(pady=8)

        combo_cat = ctk.CTkComboBox(modal, values=["Materiales", "Medicamentos", "Desechables", "Instrumental"], width=300)
        combo_cat.set(mat["categoria"])
        combo_cat.pack(pady=8)

        def _actualizar():
            nom = entry_nombre.get().strip()
            cant_str = entry_cant.get().strip()
            cat = combo_cat.get()
            try:
                cant = int(cant_str)
            except ValueError:
                messagebox.showwarning("Atención", "La cantidad debe ser un entero.")
                return

            InventarioService.actualizar_material(mat["id"], nom, cant, cat)
            modal.destroy()
            self._filtrar_inventario()

        ctk.CTkButton(modal, text="Actualizar Insumo", fg_color=THEME["primary"], height=36, command=_actualizar).pack(pady=15)

    # ==========================================
    # 5. GESTIÓN DE EQUIPO MÉDICO (AGREGAR Y QUITAR DOCTORES)
    # ==========================================
    def _render_nuevo_doctor_modal(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        lbl = ctk.CTkLabel(header, text="Gestión del Personal Médico", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(side="left")

        lbl_sub = ctk.CTkLabel(header, text="Administración de cuentas de odontólogos", font=ctk.CTkFont(size=12), text_color="#64748B")
        lbl_sub.pack(side="left", padx=15, pady=(4, 0))

        # Contenedor dividido en 2 columnas
        grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=3)
        grid.grid_columnconfigure(1, weight=2)

        # Columna 0: Lista de Doctores Activos
        col_lista = ctk.CTkFrame(grid, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12)
        col_lista.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ctk.CTkLabel(
            col_lista,
            text="👨‍⚕️ Odontólogos Registrados en el Consultorio",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))

        scroll_docs = ctk.CTkScrollableFrame(col_lista, fg_color="transparent")
        scroll_docs.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        doctores = AuthService.obtener_doctores_detalle()
        usuario_actual = self.usuario.get("usuario", "")

        for doc in doctores:
            card = ctk.CTkFrame(scroll_docs, fg_color=("#FFFFFF", "#0F172A"), corner_radius=8)
            card.pack(fill="x", padx=4, pady=4)

            info_f = ctk.CTkFrame(card, fg_color="transparent")
            info_f.pack(side="left", padx=12, pady=10, fill="x", expand=True)

            ctk.CTkLabel(info_f, text=f"🩺 {doc['nombre']}", font=ctk.CTkFont(size=13, weight="bold"), anchor="w").pack(anchor="w")
            ctk.CTkLabel(info_f, text=f"Usuario: @{doc['usuario']}", font=ctk.CTkFont(size=11), text_color="#64748B", anchor="w").pack(anchor="w")

            # Si es el Administrador Principal (Dueño)
            if doc.get("es_admin_principal"):
                ctk.CTkLabel(
                    card,
                    text="👑 Dueño / Admin",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#F59E0B"
                ).pack(side="right", padx=12)
            elif doc["usuario"] == usuario_actual:
                ctk.CTkLabel(
                    card,
                    text="👤 (Tu Sesión)",
                    font=ctk.CTkFont(size=11),
                    text_color="#0284C7"
                ).pack(side="right", padx=12)
            else:
                # Botón para Dar de Baja / Quitar Doctor
                btn_quitar = ctk.CTkButton(
                    card,
                    text="🗑️ Dar de Baja",
                    width=90,
                    height=28,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color="#EF4444",
                    hover_color="#DC2626",
                    command=lambda did=doc["id"], dnom=doc["nombre"]: self._dar_de_baja_doctor(did, dnom)
                )
                btn_quitar.pack(side="right", padx=12)

        # Columna 1: Formulario para Agregar Nuevo Doctor
        col_form = ctk.CTkFrame(grid, fg_color=("#F8FAFC", "#1E293B"), corner_radius=12)
        col_form.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            col_form,
            text="➕ Registrar Nuevo Doctor",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 4))

        ctk.CTkLabel(
            col_form,
            text="Crea una cuenta para un odontólogo del equipo.",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        ).pack(anchor="w", padx=16, pady=(0, 16))

        entry_nom = ctk.CTkEntry(col_form, width=300, height=38, placeholder_text="Nombre completo (ej: Dra. Gómez)")
        entry_nom.pack(padx=16, pady=6, fill="x")

        entry_usr = ctk.CTkEntry(col_form, width=300, height=38, placeholder_text="Nombre de usuario único")
        entry_usr.pack(padx=16, pady=6, fill="x")

        entry_pwd = ctk.CTkEntry(col_form, width=300, height=38, placeholder_text="Contraseña", show="•")
        entry_pwd.pack(padx=16, pady=6, fill="x")

        lbl_msg = ctk.CTkLabel(col_form, text="", font=ctk.CTkFont(size=11), text_color=THEME["danger"])
        lbl_msg.pack(pady=4)

        def _crear_doc():
            nom = entry_nom.get().strip()
            usr = entry_usr.get().strip()
            pwd = entry_pwd.get().strip()

            if not nom or not usr or not pwd:
                lbl_msg.configure(text="Todos los campos son requeridos.", text_color=THEME["danger"])
                return

            ok = AuthService.registrar_doctor(nom, usr, pwd)
            if ok:
                messagebox.showinfo("Éxito", f"¡Doctor '{nom}' dado de alta exitosamente!")
                self.show_view("nuevo_doctor")
            else:
                lbl_msg.configure(text="Error: El usuario ya existe.", text_color=THEME["danger"])

        ctk.CTkButton(
            col_form,
            text="Crear y Activar Doctor",
            fg_color=THEME["secondary"],
            height=40,
            command=_crear_doc
        ).pack(padx=16, pady=(12, 20), fill="x")

    def _dar_de_baja_doctor(self, id_doctor, nombre_doctor):
        confirmacion = messagebox.askyesno(
            "Confirmar Baja de Doctor",
            f"¿Estás seguro de dar de baja al doctor '{nombre_doctor}'?\n\n"
            "Ya no podrá iniciar sesión ni acceder al sistema del consultorio."
        )
        if confirmacion:
            ok, mensaje = AuthService.eliminar_doctor(id_doctor, self.usuario.get("usuario", ""))
            if ok:
                messagebox.showinfo("Baja Exitosa", mensaje)
                self.show_view("nuevo_doctor")
            else:
                messagebox.showerror("No se pudo dar de baja", mensaje)