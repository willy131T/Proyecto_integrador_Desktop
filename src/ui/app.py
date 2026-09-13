import customtkinter as ctk
from config.settings import APP_NAME
from src.ui.views.login_view import LoginView
from src.ui.views.registro_view import RegistroView
from src.ui.views.doctor_dashboard import DoctorDashboard
from src.ui.views.paciente_dashboard import PacienteDashboard
from src.ui.components.sidebar import Sidebar

class OdontoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} • Sistema de Gestión Odontológica")
        self.geometry("1180x750")
        self.minsize(1000, 650)

        # Configuración inicial de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.usuario_actual = None
        self.current_view = None
        self.sidebar = None
        self.main_container = None

        self.show_login()

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear_window()
        self.usuario_actual = None
        self.current_view = LoginView(
            self,
            on_login_success=self.on_login_success,
            on_go_register=self.show_register
        )

    def show_register(self):
        self._clear_window()
        self.current_view = RegistroView(
            self,
            on_registro_success=lambda usr: self.show_login(),
            on_go_login=self.show_login
        )

    def on_login_success(self, user_data):
        self.usuario_actual = user_data
        self._clear_window()

        # Layout autenticado: Sidebar a la izquierda, Contenido a la derecha
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            usuario=self.usuario_actual,
            on_navigate=self.on_navigate,
            on_logout=self.show_login
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Contenedor principal de la vista
        if self.usuario_actual.get("rol") == "dentista":
            self.dashboard = DoctorDashboard(self, usuario=self.usuario_actual)
        else:
            self.dashboard = PacienteDashboard(self, usuario=self.usuario_actual)

        self.dashboard.grid(row=0, column=1, sticky="nsew")
        self.sidebar.select_item("dashboard")

    def on_navigate(self, view_id):
        if hasattr(self, 'dashboard') and self.dashboard:
            self.dashboard.show_view(view_id)