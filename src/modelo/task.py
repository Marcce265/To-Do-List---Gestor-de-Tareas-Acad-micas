# Desarrollado por: Kevin Gerard Marin - HU-002
class Materia:
    """
    Representa una 'Categoría' según el glosario del proyecto.
    Alineado al Modelo Conceptual (id: int, nombre: str).
    """
    def __init__(self, nombre, color, id=None):
        self.id = id          # ID único generado por la base de datos
        self.nombre = nombre
        self.color = color