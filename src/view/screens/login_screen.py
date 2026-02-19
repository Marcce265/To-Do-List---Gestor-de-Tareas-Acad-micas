import flet as ft
from src.view.components.dialogs import show_user_dialog

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.usuarios = []
    
    def build(self):
        self._load_usuarios()
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._build_header(),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self._build_user_list(),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self._build_actions(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=30,
            expand=True,
        )
    
    def _build_header(self):
        return ft.Column(
            controls=[
                ft.Icon(
                    name=ft.icons.ASSIGNMENT,  # Cambiado de ASSIGNMENT_TURNED_IN
                    size=80,
                    color=ft.Colors.BLUE_600,
                ),
                ft.Text(
                    "Task Manager",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_600,
                ),
                ft.Text(
                    "Gestiona tus tareas académicas de manera eficiente",
                    size=16,
                    color=ft.Colors.GREY_600,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _load_usuarios(self):
        """Carga la lista de usuarios"""
        try:
            self.usuarios = self.app.task_manager.listar_usuarios()
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            self.usuarios = []
    
    def _build_user_list(self):
        if not self.usuarios:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=ft.icons.PEOPLE,  # Cambiado de PEOPLE_OUTLINE
                            size=50,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text(
                            "No hay usuarios registrados",
                            size=18,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Text(
                            "¡Crea uno nuevo!",
                            size=14,
                            color=ft.Colors.GREY_500,
                            italic=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=30,
            )
        
        user_cards = []
        for usuario in self.usuarios:
            user_cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.ListTile(
                            leading=ft.CircleAvatar(
                                content=ft.Text(usuario.nombre[0].upper()),
                                bgcolor=ft.Colors.BLUE_100,
                                color=ft.Colors.BLUE_600,
                            ),
                            title=ft.Text(usuario.nombre, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(usuario.correo),
                            on_click=lambda _, u=usuario: self._select_user(u),
                        ),
                        padding=0,
                    ),
                    elevation=3,
                    margin=5,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                controls=user_cards,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            height=300,
            width=400,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=10,
        )
    
    def _build_actions(self):
        return ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Nuevo Usuario",
                    icon=ft.icons.PERSON_ADD,
                    on_click=self._show_create_user_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        padding=20,
                    ),
                ),
                ft.OutlinedButton(
                    text="Salir",
                    icon=ft.icons.EXIT_TO_APP,
                    on_click=lambda _: self.app.page.window_close(),
                    style=ft.ButtonStyle(
                        padding=20,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    
    def _select_user(self, usuario):
        """Selecciona un usuario y va a la pantalla principal"""
        try:
            selected = self.app.task_manager.seleccionar_usuario(usuario.idUsuario)
            if selected:
                self.app.show_snackbar(f"¡Bienvenido {selected.nombre}!", ft.Colors.GREEN)
                self.app._show_main_screen()
        except Exception as e:
            self.app.show_snackbar(str(e), ft.Colors.RED_600)
    
    def _show_create_user_dialog(self, e):
        """Muestra diálogo para crear usuario"""
        def create_user(nombre, correo):
            try:
                usuario = self.app.task_manager.crear_usuario(nombre, correo)
                self._load_usuarios()
                self.app.page.update()
                self._select_user(usuario)
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        show_user_dialog(self.app.page, create_user)