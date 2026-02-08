# Desarrollado por: Kevin Gerard Marin - HU-002
import sqlite3
from src.modelo.task import Materia

class TaskManager:
    def __init__(self):
        # Conectamos a la base de datos mencionada en el Sprint Backlog
        self.conexion = sqlite3.connect('DB.sqlite')
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        # Alineado al Glosario y Modelo Conceptual: id (int) y nombre (str)
        query = '''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            color TEXT NOT NULL
        )
        '''
        self.cursor.execute(query)
        self.conexion.commit()

    def crear_materia(self, nombre, color):
        """
        HU-002: Crear Materia.
        Valida datos y retorna el objeto con su ID de base de datos.
        """
        if not nombre:
            raise ValueError("El nombre de la materia es obligatorio")
        if not color:
            raise ValueError("El color es obligatorio")

        try:
            self.cursor.execute(
                "INSERT INTO materias (nombre, color) VALUES (?, ?)",
                (nombre, color)
            )
            self.conexion.commit()
            
            # ESTA ES LA CLAVE: Recuperamos el ID que generó SQLite
            id_generado = self.cursor.lastrowid
            
            # Retornamos el objeto completo con su ID (Fase Azul)
            return Materia(nombre, color, id_generado)
            
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {e}")

    def __del__(self):
        if hasattr(self, 'conexion'):
            self.conexion.close()