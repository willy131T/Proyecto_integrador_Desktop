import customtkinter as ctk
from config.settings import THEME, APP_NAME
from src.services.auth_service import AuthService

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, on_go_register):
        super().__init__(parent, fg_color=("white", "#0F172A"))
        self.on_login_success = on_login_success
        self.on_go_register = on_go_register

        self.pack(fill="both", expand=True)

        # Contenedor central
        self.center_card = ctk.CTkFrame(
            self,
            width=420,
            corner_radius=16,
            fg_color=("#F8FAFC", "#1E293B"),
            border_width=1,
            border_color=("#E2E8F0", "#334155")
        )
        self.center_card.place(relx=0.5, rely=0.5, anchor="center")

        # Icono y Encabezado
        self.lbl_icon = ctk.CTkLabel(
            self.center_card,
            text="🦷",
            font=ctk.CTkFont(size=44)
        )
        self.lbl_icon.pack(pady=(30, 5))

        self.lbl_titulo = ctk.CTkLabel(
            self.center_card,
            text=APP_NAME,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["primary"]
        )
        self.lbl_titulo.pack(pady=(0, 2))

        self.lbl_subtitulo = ctk.CTkLabel(
            self.center_card,
            text="Inicia sesión para acceder a tu expediente o consultorio",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.lbl_subtitulo.pack(pady=(0, 25))

        # Inputs
        self.entry_usuario = ctk.CTkEntry(
            self.center_card,
            width=320,
            height=40,
            placeholder_text="Nombre de usuario",
            corner_radius=8
        )
        self.entry_usuario.pack(pady=8)

        self.entry_password = ctk.CTkEntry(
            self.center_card,
            width=320,
            height=40,
            placeholder_text="Contraseña",
            show="•",
            corner_radius=8
        )
        self.entry_password.pack(pady=8)
        self.entry_password.bind("<Return>", lambda event: self._do_login())

        # Mensaje de error
        self.lbl_error = ctk.CTkLabel(
            self.center_card,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=THEME["danger"]
        )
        self.lbl_error.pack(pady=4)

        # Botón Ingresar
        self.btn_login = ctk.CTkButton(
            self.center_card,
            text="Iniciar Sesión",
            width=320,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            corner_radius=8,
            command=self._do_login
        )
        self.btn_login.pack(pady=(10, 15))

        # Enlace a Registro
        self.btn_registro = ctk.CTkButton(
            self.center_card,
            text="¿No tienes cuenta? Regístrate aquí como paciente",
            fg_color="transparent",
            text_color=THEME["primary"],
            hover=False,
            font=ctk.CTkFont(size=12, underline=True),
            command=self.on_go_register
        )
        self.btn_registro.pack(pady=(0, 20))

        # Atajos Rápidos de Prueba
        self.frame_demo = ctk.CTkFrame(self.center_card, fg_color="transparent")
        self.frame_demo.pack(pady=(0, 20))

        self.lbl_demo = ctk.CTkLabel(self.frame_demo, text="Acceso rápido demo:", font=ctk.CTkFont(size=10), text_color="#64748B")
        self.lbl_demo.pack(side="left", padx=4)

        self.btn_demo_doc = ctk.CTkButton(
            self.frame_demo,
            text="Doctor",
            width=65,
            height=24,
            font=ctk.CTkFont(size=10),
            fg_color="#0D9488",
            command=lambda: self._fill_credentials("admin_doctor", "12345")
        )
        self.btn_demo_doc.pack(side="left", padx=4)

        self.btn_demo_pac = ctk.CTkButton(
            self.frame_demo,
            text="Paciente",
            width=65,
            height=24,
            font=ctk.CTkFont(size=10),
            fg_color="#0284C7",
            command=lambda: self._fill_credentials("william_p", "12345")
        )
        self.btn_demo_pac.pack(side="left", padx=4)

    def _fill_credentials(self, user, pwd):
        self.entry_usuario.delete(0, "end")
        self.entry_usuario.insert(0, user)
        self.entry_password.delete(0, "end")
        self.entry_password.insert(0, pwd)
        self.lbl_error.configure(text="")

    def _do_login(self):
        user = self.entry_usuario.get().strip()
        pwd = self.entry_password.get().strip()

        if not user or not pwd:
            self.lbl_error.configure(text="Por favor ingresa usuario y contraseña.")
            return

        usuario_obj = AuthService.iniciar_sesion(user, pwd)
        if usuario_obj:
            self.lbl_error.configure(text="")
            user_data = {
                "id": usuario_obj.id,
                "nombre": usuario_obj.nombre,
                "usuario": usuario_obj.usuario,
                "rol": usuario_obj.rol,
                "edad": usuario_obj.edad,
                "alergias": usuario_obj.alergias,
                "tratamiento": usuario_obj.tratamiento
            }
            self.on_login_success(user_data)
        else:
            self.lbl_error.configure(text="Credenciales incorrectas. Intenta de nuevo.")