from datetime import date
import unittest
from src.logic.task_manager import TaskManager
from src.model.declarative_base import Base, engine
from src.model.modelo import Usuario  # Importamos para aserciones


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Prepara la base de datos para cada prueba."""
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.tm = TaskManager()

    def test_hu001_rojo_crear_usuario_nombre_vacio(self):
        """
        HU-001 - Caso rojo
        No se debe permitir crear usuario con nombre vacío
        """
        with self.assertRaises(ValueError) as context:
            self.tm.crear_usuario("", "test@mail.com")
        self.assertIn("nombre", str(context.exception).lower())

    def test_hu001_rojo_crear_usuario_correo_vacio(self):
        """
        HU-001 - Caso rojo
        No se debe permitir crear usuario con correo vacío
        """
        with self.assertRaises(ValueError) as context:
            self.tm.crear_usuario("Test User", "")
        self.assertIn("correo", str(context.exception).lower())

    def test_hu001_rojo_crear_usuario_correo_duplicado(self):
        """
        HU-001 - Caso rojo
        No se debe permitir crear usuario con correo ya registrado
        """
        self.tm.crear_usuario("Juan", "test@mail.com")

        with self.assertRaises(ValueError) as context:
            self.tm.crear_usuario("Pedro", "test@mail.com")
        self.assertIn("correo", str(context.exception).lower())

    def test_hu001_verde_crear_usuario_caso_feliz(self):
        """
        HU-001 - Caso verde
        Crear usuario con datos válidos
        """
        usuario = self.tm.crear_usuario("Juan Pérez", "juan@mail.com")

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Juan Pérez")
        self.assertEqual(usuario.correo, "juan@mail.com")
        self.assertIsNotNone(usuario.fecha_creacion)

    def test_hu002_rojo_seleccionar_usuario_id_cero(self):
        """
        HU-002 - Caso rojo
        No se debe permitir ID cero
        """
        with self.assertRaises(ValueError) as context:
            self.tm.seleccionar_usuario(0)
        self.assertIn("id", str(context.exception).lower())

    def test_hu002_rojo_seleccionar_usuario_id_negativo(self):
        """
        HU-002 - Caso rojo
        No se debe permitir ID negativo
        """
        with self.assertRaises(ValueError) as context:
            self.tm.seleccionar_usuario(-5)
        self.assertIn("id", str(context.exception).lower())

    def test_hu002_rojo_seleccionar_usuario_inexistente(self):
        """
        HU-002 - Caso rojo
        Debe retornar None si el usuario no existe
        """
        usuario = self.tm.seleccionar_usuario(999)
        self.assertIsNone(usuario)

    def test_hu002_verde_seleccionar_usuario_caso_feliz(self):
        """
        HU-002 - Caso verde
        Seleccionar usuario existente por ID
        """
        usuario_creado = self.tm.crear_usuario("Juan", "juan@mail.com")
        usuario = self.tm.seleccionar_usuario(usuario_creado.idUsuario)

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.correo, "juan@mail.com")

    def test_hu003_rojo_crear_materia_usuario_inexistente(self):
        """
        HU-003 - Caso rojo
        No se debe permitir crear materia sin usuario válido
        """
        with self.assertRaises(ValueError) as context:
            self.tm.crear_materia(999, "Matemáticas", "Azul")

        self.assertIn("usuario", str(context.exception).lower())

    def test_hu003_rojo_crear_materia_nombre_vacio(self):
        """
        HU-003 - Caso rojo
        No se debe permitir crear materia con nombre vacío
        """
        usuario = self.tm.crear_usuario("Juan", "juan@mail.com")

        with self.assertRaises(ValueError) as context:
            self.tm.crear_materia(usuario.idUsuario, "", "Azul")

        self.assertIn("nombre", str(context.exception).lower())

    def test_hu003_rojo_crear_materia_color_vacio(self):
        """
        HU-003 - Caso rojo
        No se debe permitir crear materia con color vacío
        """
        usuario = self.tm.crear_usuario("Juan", "juan@mail.com")

        with self.assertRaises(ValueError) as context:
            self.tm.crear_materia(usuario.idUsuario, "Matemáticas", "")

        self.assertIn("color", str(context.exception).lower())

    def test_hu003_rojo_crear_materia_caso_feliz(self):
        """
        HU-003 - Caso rojo
        Crear una materia válida asociada a un usuario
        """
        usuario = self.tm.crear_usuario("Juan", "juan@mail.com")

        materia = self.tm.crear_materia(
            usuario.idUsuario,
            "Matemáticas",
            "Azul"
        )

        self.assertIsNotNone(materia)
        self.assertEqual(materia.nombre, "Matemáticas")
        self.assertEqual(materia.color, "Azul")
        self.assertEqual(materia.usuario_id, usuario.idUsuario)

    def test_hu004_rojo_crear_tarea_titulo_vacio(self):
        """
        HU-004 - Escenario 1 (Rojo)
        No se debe permitir crear una tarea con título vacío
        """
        # 1. Preparación (Setup)
        from src.model.modelo import Materia, Prioridad
        from src.model.declarative_base import session
        
        # Creamos un usuario usando el método que ya existe
        usuario = self.tm.crear_usuario("Ana", "ana@mail.com")
        
        # Creamos una materia directamente en la base de datos para la prueba
        materia = Materia(nombre="Física", color="Rojo", usuario_id=usuario.idUsuario)
        session.add(materia)
        session.commit()
        session.refresh(materia)
        materia_id = materia.idMateria

        # 2. Acción y Aserción
        with self.assertRaises(ValueError) as context:
            # Intentamos crear la tarea con título vacío
            self.tm.crear_tarea(
                titulo="", 
                descripcion="Resolver ejercicios de cinemática",
                prioridad=Prioridad.Media,
                fecha_entrega=date.today(),
                materia_id=materia_id
            )
        
        # Verificamos que el error mencione el problema con el título
        self.assertIn("título", str(context.exception).lower())

