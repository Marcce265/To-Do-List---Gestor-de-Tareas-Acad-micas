# Desarrollado por: Kevin Gerard Marin - HU-002
import unittest
from src.logica.task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()

    def test_crear_materia_exitoso(self):
        # Test de Caso Feliz
        resultado = self.task_manager.crear_materia("Matemática", "Azul")
        self.assertEqual(resultado.nombre, "Matemática")
        self.assertEqual(resultado.color, "Azul")
        # Fase Azul: Verificamos que ahora el objeto tiene un ID asignado por la BD
        self.assertIsNotNone(resultado.id)

    def test_crear_materia_nombre_vacio(self):
        # Test de Caso Infeliz 1
        with self.assertRaises(ValueError):
            self.task_manager.crear_materia("", "Verde")

    def test_crear_materia_color_vacio(self):
        # Test de Caso Infeliz 2
        with self.assertRaises(ValueError):
            self.task_manager.crear_materia("Física", "")

if __name__ == '__main__':
    unittest.main()