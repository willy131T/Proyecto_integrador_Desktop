import customtkinter as ctk
from config.settings import THEME
from src.services.auth_service import AuthService
from src.services.paciente_service import PacienteService

class RegistroView(ctk.CTkFrame):
    def __init__(self, parent, on_registro_success, on_go_login):
        super().__init__(parent, fg_color=("white", "#0F172A"))
        self.on_registro_success = on_registro_success
        self.on_go_login = on_go_login

        self.pack(fill="both", expand=True)

        self.center_card = ctk.CTkFrame(
            self,
            width=460,
            corner_radius=16,
            fg_color=("#F8FAFC", "#1E293B"),
            border_width=1,
            border_color=("#E2E8F0", "#334155")
        )
        self.center_card.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(
            self.center_card,
            text="Registro de Nuevo Paciente",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME["primary"]
        )
        self.lbl_titulo.pack(pady=(25, 4))

        self.lbl_sub = ctk.CTkLabel(
            self.center_card,
            text="Completa tu ficha para agendar tus citas dentales",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.lbl_sub.pack(pady=(0, 20))

        # Campos
        self.entry_nombre = ctk.CTkEntry(self.center_card, width=340, height=38, placeholder_text="Nombre completo")
        self.entry_nombre.pack(pady=6)

        self.entry_usuario = ctk.CTkEntry(self.center_card, width=340, height=38, placeholder_text="Usuario único")
        self.entry_usuario.pack(pady=6)

        self.entry_password = ctk.CTkEntry(self.center_card, width=340, height=38, placeholder_text="Contraseña", show="•")
        self.entry_password.pack(pady=6)

        self.entry_edad = ctk.CTkEntry(self.center_card, width=340, height=38, placeholder_text="Edad (años)")
        self.entry_edad.pack(pady=6)

        self.entry_alergias = ctk.CTkEntry(self.center_card, width=340, height=38, placeholder_text="Alergias médicas (ej: Penicilina o Ninguna)")
        self.entry_alergias.pack(pady=6)

        self.lbl_error = ctk.CTkLabel(self.center_card, text="", font=ctk.CTkFont(size=12), text_color=THEME["danger"])
        self.lbl_error.pack(pady=4)

        # Botón Registrar
        self.btn_registrar = ctk.CTkButton(
            self.center_card,
            text="Completar Registro",
            width=340,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            corner_radius=8,
            command=self._do_register
        )
        self.btn_registrar.pack(pady=(8, 12))

        # Volver al login
        self.btn_volver = ctk.CTkButton(
            self.center_card,
            text="¿Ya tienes una cuenta? Inicia sesión aquí",
            fg_color="transparent",
            text_color=THEME["primary"],
            hover=False,
            font=ctk.CTkFont(size=12, underline=True),
            command=self.on_go_login
        )
        self.btn_volver.pack(pady=(0, 20))

    def _do_register(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        edad_str = self.entry_edad.get().strip()
        alergias = self.entry_alergias.get().strip() or "Ninguna"

        if not nombre or not usuario or not password or not edad_str:
            self.lbl_error.configure(text="Por favor llena todos los campos obligatorios.")
            return

        try:
            edad = int(edad_str)
            if edad < 0 or edad > 125:
                raise ValueError()
        except ValueError:
            self.lbl_error.configure(text="Por favor ingresa una edad numérica válida.")
            return

        # Registrar en usuarios
        ok_user = AuthService.registrar_paciente(nombre, usuario, password, edad, alergias)
        if not ok_user:
            self.lbl_error.configure(text="El nombre de usuario ya está registrado. Elige otro.")
            return

        # Registrar en directorio de pacientes
        PacienteService.registrar_o_actualizar_paciente(nombre, edad, alergias)

        self.on_registro_success(usuario)