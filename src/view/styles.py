import flet as ft

class app_theme:
    @staticmethod
    def get_theme() -> ft.Theme:
        """Tema principal de la aplicación - Versión mínima"""
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.BLUE_600,
                secondary=ft.Colors.TEAL_600,
                error=ft.Colors.RED_600,
                surface=ft.Colors.WHITE,
            ),
            use_material3=True,
        )
    
    @staticmethod
    def get_priority_color(prioridad: str) -> str:
        """Retorna color según prioridad"""
        colors = {
            "Alta": ft.Colors.RED_600,
            "Media": ft.Colors.ORANGE_600,
            "Baja": ft.Colors.GREEN_600,
        }
        return colors.get(prioridad, ft.Colors.GREY_600)
    
    @staticmethod
    def get_estado_color(estado: str) -> str:
        """Retorna color según estado"""
        return ft.Colors.GREEN_600 if estado == "Completada" else ft.Colors.ORANGE_600
    
    @staticmethod
    def get_priority_icon(prioridad: str) -> str:
        """Retorna icono según prioridad"""
        icons = {
            "Alta": ft.icons.PRIORITY_HIGH,
            "Media": ft.icons.REMOVE,
            "Baja": ft.icons.LOW_PRIORITY,
        }
        return icons.get(prioridad, ft.icons.HELP)