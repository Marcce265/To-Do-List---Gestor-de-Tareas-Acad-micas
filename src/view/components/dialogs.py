import flet as ft
from datetime import date, datetime

def show_user_dialog(page: ft.Page, on_submit):
    """Diálogo para crear/editar usuario"""
    nombre_field = ft.TextField(
        label="Nombre completo",
        hint_text="Ej: Juan Pérez",
        prefix_icon=ft.icons.PERSON,
        autofocus=True,
        width=400,
    )
    
    correo_field = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo@correo.com",
        prefix_icon=ft.icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL,
        width=400,
    )
    
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    def submit(e):
        if not nombre_field.value or not correo_field.value:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Todos los campos son obligatorios"))
            )
            return
        
        on_submit(nombre_field.value.strip(), correo_field.value.strip())
        close_dialog(e)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Nuevo Usuario"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    nombre_field,
                    correo_field,
                ],
                tight=True,
                spacing=20,
            ),
            padding=20,
            width=450,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dialog),
            ft.ElevatedButton("Crear", on_click=submit),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()


def show_materia_dialog(page: ft.Page, on_submit, materia=None):
    """Diálogo para crear/editar materia"""
    nombre_field = ft.TextField(
        label="Nombre de la materia",
        hint_text="Ej: Matemáticas",
        prefix_icon=ft.icons.BOOK,
        autofocus=True,
        value=materia.nombre if materia else "",
        width=400,
    )
    
    # Selector de color
    color_picker = ft.Dropdown(
        label="Color",
        value=materia.color[1:] if materia else "3498db",  # Quitamos el # para el dropdown
        options=[
            ft.dropdown.Option("e74c3c", "🔴 Rojo"),
            ft.dropdown.Option("3498db", "🔵 Azul"),
            ft.dropdown.Option("2ecc71", "🟢 Verde"),
            ft.dropdown.Option("f39c12", "🟡 Naranja"),
            ft.dropdown.Option("9b59b6", "🟣 Morado"),
            ft.dropdown.Option("e67e22", "🟠 Naranja oscuro"),
        ],
        width=400,
    )
    
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    def submit(e):
        if not nombre_field.value:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("El nombre es obligatorio"))
            )
            return
        
        on_submit(nombre_field.value.strip(), f"#{color_picker.value}")
        close_dialog(e)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Nueva Materia" if not materia else "Editar Materia"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    nombre_field,
                    color_picker,
                ],
                tight=True,
                spacing=20,
            ),
            padding=20,
            width=450,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dialog),
            ft.ElevatedButton("Guardar", on_click=submit),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()


def show_tarea_dialog(page: ft.Page, on_submit, materias, tarea=None):
    """Diálogo para crear/editar tarea"""
    titulo_field = ft.TextField(
        label="Título",
        hint_text="Ej: Examen final",
        prefix_icon=ft.icons.TITLE,
        autofocus=True,
        value=tarea.titulo if tarea else "",
        width=500,
    )
    
    descripcion_field = ft.TextField(
        label="Descripción",
        hint_text="Detalles de la tarea...",
        prefix_icon=ft.icons.DESCRIPTION,
        multiline=True,
        min_lines=3,
        max_lines=5,
        value=tarea.descripcion if tarea else "",
        width=500,
    )
    
    # Selector de materia
    materia_options = [
        ft.dropdown.Option(str(m.idMateria), m.nombre) 
        for m in materias
    ]
    
    materia_dropdown = ft.Dropdown(
        label="Materia",
        value=str(tarea.materia_id) if tarea else str(materias[0].idMateria),
        options=materia_options,
        prefix_icon=ft.icons.BOOK,
        width=500,
    )
    
    # Selector de prioridad
    prioridad_dropdown = ft.Dropdown(
        label="Prioridad",
        value=tarea.prioridad.value if tarea else "Media",
        options=[
            ft.dropdown.Option("Baja", "🔵 Baja"),
            ft.dropdown.Option("Media", "🟡 Media"),
            ft.dropdown.Option("Alta", "🔴 Alta"),
        ],
        prefix_icon=ft.icons.FLAG,  # Cambiado de PRIORITY_HIGH
        width=500,
    )
    
    # Selector de fecha
    today = date.today()
    fecha_field = ft.TextField(
        label="Fecha de entrega",
        value=tarea.fechaEntrega.strftime("%Y-%m-%d") if tarea else today.strftime("%Y-%m-%d"),
        read_only=True,
        prefix_icon=ft.icons.CALENDAR_TODAY,
        width=500,
    )
    
    def handle_date_change(e):
        if e.control.value:
            fecha_field.value = e.control.value.strftime("%Y-%m-%d")
            page.update()
    
    date_picker = ft.DatePicker(
        first_date=today,
        last_date=date(today.year + 2, 12, 31),
        on_change=handle_date_change,
    )
    page.overlay.append(date_picker)
    
    def open_date_picker(e):
        date_picker.pick_date()
    
    fecha_field.on_click = open_date_picker
    
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    def submit(e):
        if not titulo_field.value:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("El título es obligatorio"))
            )
            return
        
        try:
            fecha = datetime.strptime(fecha_field.value, "%Y-%m-%d").date()
            on_submit(
                titulo_field.value.strip(),
                descripcion_field.value.strip() if descripcion_field.value else "",
                int(materia_dropdown.value),
                prioridad_dropdown.value,
                fecha,
            )
            close_dialog(e)
        except Exception as ex:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Error en fecha: {str(ex)}"))
            )
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Nueva Tarea" if not tarea else "Editar Tarea"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    titulo_field,
                    descripcion_field,
                    materia_dropdown,
                    prioridad_dropdown,
                    fecha_field,
                ],
                tight=True,
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            width=550,
            height=500,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dialog),
            ft.ElevatedButton("Guardar", on_click=submit),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()


def show_confirm_dialog(page: ft.Page, title: str, message: str, on_confirm):
    """Diálogo de confirmación"""
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    def confirm(e):
        on_confirm()
        close_dialog(e)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dialog),
            ft.ElevatedButton("Confirmar", on_click=confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()