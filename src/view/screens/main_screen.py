import flet as ft
from src.view.components.dialogs import show_materia_dialog, show_confirm_dialog
from src.model.modelo import Materia
from sqlalchemy.orm import sessionmaker
from src.model.declarative_base import engine

Session = sessionmaker(bind=engine)

class MainScreen:
    def __init__(self, app):
        self.app = app
        self.materias = []
    
    def build(self):
        self._load_materias()
        
        return ft.Column(
            controls=[
                self._build_app_bar(),
                self._build_materias_grid(),
            ],
            expand=True,
        )
    
    def _build_app_bar(self):
        usuario = self.app.task_manager.usuario_activo
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Text(usuario.nombre[0].upper()),
                                bgcolor=ft.Colors.BLUE_100,
                                color=ft.Colors.BLUE_600,
                                radius=25,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        usuario.nombre,
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        usuario.correo,
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar perfil",
                                on_click=self._edit_profile,
                            ),
                            ft.IconButton(
                                icon=ft.icons.LOGOUT,
                                tooltip="Cerrar sesión",
                                on_click=self._logout,
                            ),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=20),
        )
    
    def _load_materias(self):
        """Carga las materias del usuario activo"""
        session = Session()
        try:
            self.materias = session.query(Materia).filter_by(
                usuario_id=self.app.task_manager.usuario_activo.idUsuario
            ).all()
        finally:
            session.close()
    
    def _build_materias_grid(self):
        if not self.materias:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=ft.icons.FOLDER,  # Cambiado de FOLDER_OPEN
                            size=64,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text(
                            "No tienes materias creadas",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Text(
                            "Crea tu primera materia para comenzar",
                            size=16,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.ElevatedButton(
                            text="Crear Primera Materia",
                            icon=ft.icons.ADD,
                            on_click=self._show_create_materia_dialog,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                padding=20,
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        
        # Crear grid de materias
        materias_grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=300,
            spacing=15,
            run_spacing=15,
            child_aspect_ratio=1.2,
        )
        
        for materia in self.materias:
            materias_grid.controls.append(
                self._build_materia_card(materia)
            )
        
        # Stack con grid y botón flotante
        return ft.Stack(
            controls=[
                materias_grid,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=self._show_create_materia_dialog,
                    bgcolor=ft.Colors.BLUE_600,
                    foreground_color=ft.Colors.WHITE,
                ),
            ],
            expand=True,
        )
    
    def _build_materia_card(self, materia):
        # Contar tareas pendientes
        tareas_pendientes = sum(
            1 for t in materia.tareas 
            if t.estado.value == "Pendiente"
        )
        tareas_totales = len(materia.tareas)
        
        progreso = (tareas_totales - tareas_pendientes) / max(tareas_totales, 1)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        width=20,
                                        height=20,
                                        bgcolor=materia.color,
                                        border_radius=10,
                                    ),
                                    ft.Text(
                                        materia.nombre,
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        expand=True,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=10,
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.icons.TASK,  # Este existe
                                                size=20,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                f"Tareas totales: {tareas_totales}",
                                                size=14,
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.icons.HOURGLASS_EMPTY,  # Cambiado de PENDING_ACTIONS
                                                size=20,
                                                color=ft.Colors.ORANGE_600,
                                            ),
                                            ft.Text(
                                                f"Pendientes: {tareas_pendientes}",
                                                size=14,
                                                color=ft.Colors.ORANGE_600,
                                            ),
                                        ],
                                    ),
                                    ft.ProgressBar(
                                        value=progreso,
                                        color=ft.Colors.GREEN_600,
                                        bgcolor=ft.Colors.GREY_300,
                                    ),
                                ],
                                spacing=10,
                            ),
                            padding=10,
                        ),
                    ],
                ),
                on_click=lambda _, m=materia: self.app.navigate_to_materia(m.idMateria),
            ),
            elevation=4,
        )
    
    def _show_create_materia_dialog(self, e):
        """Muestra diálogo para crear materia"""
        def create_materia(nombre, color):
            try:
                materia = self.app.task_manager.crear_materia(nombre, color)
                self._load_materias()
                self.app.page.update()
                self.app.show_snackbar(f"Materia '{nombre}' creada exitosamente")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        show_materia_dialog(self.app.page, create_materia)
    
    def _edit_profile(self, e):
        """Editar perfil de usuario"""
        self.app.show_snackbar("Funcionalidad en desarrollo", ft.Colors.ORANGE_600)
    
    def _logout(self, e):
        """Cerrar sesión"""
        self.app.task_manager.usuario_activo = None
        self.app._show_login_screen()