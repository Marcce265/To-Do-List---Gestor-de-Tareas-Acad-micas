import unittest
from src.logica.task_manager import TaskManager
from src.modelo.declarative_base import Base, engine


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        self.tm = TaskManager()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_hu001_rojo_sin_perfiles(self):
        perfil = self.tm.seleccionar_perfil(1)
        self.assertIsNone(perfil)

    def test_hu001_verde_crear_perfil(self):
        perfil = self.tm.crear_perfil("Ernesto")
        self.assertIsNotNone(perfil)
    
    def test_hu001_seleccionar_perfil_id_invalido(self):
        with self.assertRaises(ValueError):
            self.tm.seleccionar_perfil(0)

    def test_hu002_escenario1_crear_materia_valida(self):
        # Escenario 1: Datos válidos (Rojo)
        resultado = self.tm.crear_materia(nombre="Matemáticas", descripcion="Cálculo I")
        self.assertTrue(resultado)
    def test_hu002_escenario2_nombre_obligatorio(self):
        # Escenario 2: No debe permitir nombres vacíos
        with self.assertRaises(ValueError):
            self.tm.crear_materia(nombre="", descripcion="Sin nombre")
        

