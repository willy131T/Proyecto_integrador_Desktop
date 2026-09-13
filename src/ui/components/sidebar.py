import customtkinter as ctk
from config.settings import THEME, APP_NAME

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, usuario, on_navigate, on_logout):
        super().__init__(parent, width=220, corner_radius=0, fg_color=("#F1F5F9", "#0F172A"))
        self.usuario = usuario
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.buttons = {}

        self.grid_rowconfigure(8, weight=1)

        # Encabezado con Logotipo
        self.lbl_logo = ctk.CTkLabel(
            self,
            text=f"🦷 {APP_NAME.split()[0]}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME["primary"]
        )
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(25, 5), sticky="w")

        self.lbl_sub = ctk.CTkLabel(
            self,
            text="Gestión Odontológica Pro",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.lbl_sub.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Tarjeta de Usuario
        self.user_card = ctk.CTkFrame(self, fg_color=("#E2E8F0", "#1E293B"), corner_radius=10)
        self.user_card.grid(row=2, column=0, padx=15, pady=(0, 20), sticky="ew")

        rol_text = "👨‍⚕️ Odontólogo / Admin" if self.usuario.get("rol") == "dentista" else "👤 Paciente"
        self.lbl_user_name = ctk.CTkLabel(
            self.user_card,
            text=self.usuario.get("nombre", "Usuario"),
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.lbl_user_name.pack(padx=12, pady=(10, 2), fill="x")

        self.lbl_user_rol = ctk.CTkLabel(
            self.user_card,
            text=rol_text,
            font=ctk.CTkFont(size=10),
            text_color=THEME["secondary"],
            anchor="w"
        )
        self.lbl_user_rol.pack(padx=12, pady=(0, 10), fill="x")

        # Botones de Navegación según Rol
        nav_items = []
        if self.usuario.get("rol") == "dentista":
            nav_items = [
                ("dashboard", "📊 Resumen", 3),
                ("citas", "📅 Agenda de Citas", 4),
                ("pacientes", "👥 Expedientes", 5),
                ("inventario", "📦 Inventario", 6),
                ("nuevo_doctor", "👨‍⚕️ Equipo Médico", 7),
            ]
        else:
            nav_items = [
                ("dashboard", "🏠 Mi Portal", 3),
                ("mis_citas", "📅 Mis Citas", 4),
                ("agendar", "➕ Agendar Cita", 5),
            ]

        for view_id, label, row_idx in nav_items:
            btn = ctk.CTkButton(
                self,
                text=label,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color=("#1E293B", "#F8FAFC"),
                hover_color=("#CBD5E1", "#334155"),
                anchor="w",
                height=38,
                command=lambda vid=view_id: self._handle_click(vid)
            )
            btn.grid(row=row_idx, column=0, padx=12, pady=4, sticky="ew")
            self.buttons[view_id] = btn

        # Selector de Tema
        self.theme_switch = ctk.CTkSwitch(
            self,
            text="Modo Oscuro",
            font=ctk.CTkFont(size=11),
            command=self._toggle_theme
        )
        self.theme_switch.select()
        self.theme_switch.grid(row=9, column=0, padx=20, pady=(0, 15), sticky="w")

        # Botón Cerrar Sesión
        self.btn_logout = ctk.CTkButton(
            self,
            text="🚪 Cerrar Sesión",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            height=36,
            command=self.on_logout
        )
        self.btn_logout.grid(row=10, column=0, padx=15, pady=(0, 20), sticky="ew")

    def _handle_click(self, view_id):
        for vid, btn in self.buttons.items():
            if vid == view_id:
                btn.configure(fg_color=THEME["primary"], text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=("#1E293B", "#F8FAFC"))
        self.on_navigate(view_id)

    def select_item(self, view_id):
        self._handle_click(view_id)

    def _toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")