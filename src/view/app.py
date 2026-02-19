import flet as ft
from src.logic.task_manager import TaskManager
from src.view.screens.login_screen import LoginScreen
from src.view.screens.main_screen import MainScreen
from src.view.styles import app_theme
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoApp:
    def __init__(self):
        self.task_manager = TaskManager()
        self.page = None
        self.current_screen = None
    
    def main(self, page: ft.Page):
        """Punto de entrada principal de Flet"""
        self.page = page
        self._setup_page()
        self._show_login_screen()
    
    def _setup_page(self):
        """Configuración inicial de la página"""
        self.page.title = "Task Manager - Gestor de Tareas"
        self.page.theme = app_theme.get_theme()
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.window.width = 1000
        self.page.window.height = 700
        self.page.window.min_width = 600
        self.page.window.min_height = 500
        self.page.update()
    
    def _show_login_screen(self):
        """Muestra la pantalla de login/selección de usuario"""
        logger.info("Mostrando pantalla de login")
        self.current_screen = LoginScreen(self)
        self.page.clean()
        self.page.add(self.current_screen.build())
        self.page.update()
    
    def _show_main_screen(self):
        """Muestra la pantalla principal con materias"""
        logger.info(f"Mostrando pantalla principal para usuario: {self.task_manager.usuario_activo.nombre if self.task_manager.usuario_activo else 'None'}")
        self.current_screen = MainScreen(self)
        self.page.clean()
        self.page.add(self.current_screen.build())
        self.page.update()
    
    def navigate_to_materia(self, materia_id: int):
        """Navega al detalle de una materia"""
        logger.info(f"Navegando a materia ID: {materia_id}")
        from src.view.screens.materia_screen import MateriaScreen
        self.current_screen = MateriaScreen(self, materia_id)
        self.page.clean()
        self.page.add(self.current_screen.build())
        self.page.update()
    
    def go_back(self):
        """Vuelve a la pantalla anterior"""
        logger.info("Volviendo a pantalla anterior")
        if self.task_manager.usuario_activo:
            self._show_main_screen()
        else:
            self._show_login_screen()
    
    def show_snackbar(self, message: str, color: str = ft.Colors.GREEN):
        """Muestra un mensaje temporal"""
        logger.info(f"Snackbar: {message}")
        snack = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            action="OK",
            duration=3000,
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

# Usar run() en lugar de app() para evitar el DeprecationWarning
if __name__ == "__main__":
    app = TodoApp()
    ft.app(target=app.main)