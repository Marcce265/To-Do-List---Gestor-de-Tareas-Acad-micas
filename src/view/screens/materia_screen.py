import flet as ft
from src.view.components.dialogs import show_tarea_dialog, show_confirm_dialog
from src.model.modelo import Materia, Tarea
from sqlalchemy.orm import sessionmaker
from src.model.declarative_base import engine
from src.view.styles import app_theme

Session = sessionmaker(bind=engine)

class MateriaScreen:
    def __init__(self, app, materia_id: int):
        self.app = app
        self.materia_id = materia_id
        self.materia = None
        self.tareas = []
    
    def build(self):
        self._load_data()
        
        return ft.Column(
            controls=[
                self._build_app_bar(),
                self._build_tareas_list(),
            ],
            expand=True,
        )
    
    def _load_data(self):
        """Carga la materia y sus tareas"""
        session = Session()
        try:
            self.materia = session.query(Materia).filter_by(
                idMateria=self.materia_id
            ).first()
            
            self.tareas = sorted(
                self.materia.tareas,
                key=lambda t: (
                    t.estado.value == "Completada",  # Pendientes primero
                    t.fechaEntrega,                   # Luego por fecha
                )
            )
        finally:
            session.close()
    
    def _build_app_bar(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.app.go_back(),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                self.materia.nombre,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"{len(self.tareas)} tareas",
                                size=14,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar materia",
                                on_click=self._edit_materia,
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Eliminar materia",
                                on_click=self._delete_materia,
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
    
    def _build_tareas_list(self):
        if not self.tareas:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=ft.icons.ASSIGNMENT_LATE,
                            size=64,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text(
                            "No hay tareas en esta materia",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Text(
                            "Crea tu primera tarea",
                            size=16,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.ElevatedButton(
                            text="Crear Primera Tarea",
                            icon=ft.icons.ADD,
                            on_click=self._show_create_tarea_dialog,
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
        
        tareas_columna = ft.Column(
            controls=[],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # Separar tareas pendientes y completadas
        pendientes = [t for t in self.tareas if t.estado.value == "Pendiente"]
        completadas = [t for t in self.tareas if t.estado.value == "Completada"]
        
        if pendientes:
            tareas_columna.controls.append(
                ft.Text("Pendientes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_600)
            )
            for tarea in pendientes:
                tareas_columna.controls.append(
                    self._build_tarea_card(tarea, completada=False)
                )
        
        if completadas:
            tareas_columna.controls.append(
                ft.Divider(height=20)
            )
            tareas_columna.controls.append(
                ft.Text("Completadas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600)
            )
            for tarea in completadas:
                tareas_columna.controls.append(
                    self._build_tarea_card(tarea, completada=True)
                )
        
        # Botón flotante para nueva tarea
        return ft.Stack(
            controls=[
                ft.Container(
                    content=tareas_columna,
                    padding=10,
                ),
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=self._show_create_tarea_dialog,
                    bgcolor=ft.Colors.BLUE_600,
                    foreground_color=ft.Colors.WHITE,
                ),
            ],
            expand=True,
        )
    
    def _build_tarea_card(self, tarea, completada: bool = False):
        prioridad_color = app_theme.get_priority_color(tarea.prioridad.value)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=completada,
                            on_change=lambda _, t=tarea: self._toggle_tarea(t),
                            active_color=ft.Colors.GREEN_600,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    tarea.titulo,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_400 if completada else None,
                                ),
                                ft.Text(
                                    tarea.descripcion or "Sin descripción",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        name=ft.icons.FLAG,  # Cambiado
                                                        size=14,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                    ft.Text(
                                                        tarea.prioridad.value,
                                                        size=12,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                ],
                                                spacing=3,
                                            ),
                                            padding=ft.padding.only(8, 3, 8, 3),
                                            bgcolor=prioridad_color,
                                            border_radius=15,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.icons.CALENDAR_TODAY,
                                                    size=14,
                                                    color=ft.Colors.GREY_600,
                                                ),
                                                ft.Text(
                                                    tarea.fechaEntrega.strftime("%d/%m/%Y"),
                                                    size=12,
                                                    color=ft.Colors.GREY_600,
                                                ),
                                            ],
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(
                                    text="Editar",
                                    icon=ft.icons.EDIT,
                                    on_click=lambda _, t=tarea: self._edit_tarea(t),
                                ),
                                ft.PopupMenuItem(
                                    text="Eliminar",
                                    icon=ft.icons.DELETE,
                                    on_click=lambda _, t=tarea: self._delete_tarea(t),
                                ),
                            ],
                        ),
                    ],
                ),
                padding=15,
            ),
            elevation=2,
        )
    
    def _toggle_tarea(self, tarea):
        """Marca/desmarca tarea"""
        try:
            if tarea.estado.value == "Pendiente":
                self.app.task_manager.marcar_tarea(tarea.idTarea)
            else:
                self.app.task_manager.desmarcar_tarea(tarea.idTarea)
            
            self._load_data()
            self.app.page.update()
        except Exception as e:
            self.app.show_snackbar(str(e), ft.Colors.RED_600)
    
    def _show_create_tarea_dialog(self, e):
        """Muestra diálogo para crear tarea"""
        def create_tarea(titulo, descripcion, materia_id, prioridad, fecha):
            try:
                from src.model.modelo import Prioridad
                prioridad_enum = Prioridad[prioridad]
                
                tarea = self.app.task_manager.crear_tarea(
                    titulo=titulo,
                    descripcion=descripcion,
                    prioridad=prioridad_enum,
                    fecha_entrega=fecha,
                    materia_id=materia_id,
                )
                self._load_data()
                self.app.page.update()
                self.app.show_snackbar("Tarea creada exitosamente")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        # Obtener materias del usuario
        session = Session()
        try:
            materias = session.query(Materia).filter_by(
                usuario_id=self.app.task_manager.usuario_activo.idUsuario
            ).all()
            show_tarea_dialog(self.app.page, create_tarea, materias)
        finally:
            session.close()
    
    def _edit_tarea(self, tarea):
        """Edita una tarea"""
        def update_tarea(titulo, descripcion, materia_id, prioridad, fecha):
            try:
                from src.model.modelo import Prioridad
                prioridad_enum = Prioridad[prioridad]
                
                self.app.task_manager.editar_tarea(
                    id_tarea=tarea.idTarea,
                    nuevo_titulo=titulo,
                    nueva_descripcion=descripcion,
                    nueva_prioridad=prioridad_enum,
                    nueva_fecha_entrega=fecha,
                    nueva_materia_id=materia_id,
                )
                self._load_data()
                self.app.page.update()
                self.app.show_snackbar("Tarea actualizada")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        # Obtener materias del usuario
        session = Session()
        try:
            materias = session.query(Materia).filter_by(
                usuario_id=self.app.task_manager.usuario_activo.idUsuario
            ).all()
            show_tarea_dialog(self.app.page, update_tarea, materias, tarea)
        finally:
            session.close()
    
    def _delete_tarea(self, tarea):
        """Elimina una tarea"""
        def confirm_delete():
            try:
                self.app.task_manager.eliminar_tarea(tarea.idTarea)
                self._load_data()
                self.app.page.update()
                self.app.show_snackbar("Tarea eliminada")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        show_confirm_dialog(
            self.app.page,
            "Eliminar Tarea",
            f"¿Estás seguro de eliminar la tarea '{tarea.titulo}'?",
            confirm_delete,
        )
    
    def _edit_materia(self, e):
        """Edita la materia actual"""
        def update_materia(nombre, color):
            try:
                self.app.task_manager.editar_materia(
                    id_materia=self.materia_id,
                    nuevo_nombre=nombre,
                    nuevo_color=color
                )
                self._load_data()
                self.app.page.update()
                self.app.show_snackbar("Materia actualizada")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        from src.view.components.dialogs import show_materia_dialog
        show_materia_dialog(self.app.page, update_materia, self.materia)
    
    def _delete_materia(self, e):
        """Elimina la materia actual"""
        def confirm_delete():
            try:
                self.app.task_manager.eliminar_materia(self.materia_id)
                self.app.go_back()
                self.app.show_snackbar("Materia eliminada")
            except Exception as e:
                self.app.show_snackbar(str(e), ft.Colors.RED_600)
        
        show_confirm_dialog(
            self.app.page,
            "Eliminar Materia",
            f"¿Estás seguro de eliminar la materia '{self.materia.nombre}'?\n"
            "Todas las tareas asociadas también serán eliminadas.",
            confirm_delete,
        )