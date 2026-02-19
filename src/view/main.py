import flet as ft

def main(page: ft.Page):
    page.title = "To-Do List Académico"
    page.add(
        ft.Text("Hola Ernesto, Flet está funcionando 🚀")
    )

ft.app(target=main)
