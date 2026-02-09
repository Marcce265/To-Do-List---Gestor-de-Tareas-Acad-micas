from src.modelo.declarative_base import Session
from src.modelo.modelo import Perfil,Materia 


class TaskManager:
    """
    Clase que contiene la lógica de negocio para la gestión de perfiles,
    materias y tareas.
    """

    def crear_perfil(self, nombre: str) -> Perfil:
        """
        Crea un nuevo perfil de usuario.

        :param nombre: Nombre del perfil
        :return: Perfil creado
        :raises ValueError: si el nombre es vacío
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del perfil no puede estar vacío")

        session = Session()
        perfil = Perfil(nombre=nombre.strip())
        session.add(perfil)
        session.commit()
        session.refresh(perfil)
        session.close()
        return perfil

    def seleccionar_perfil(self, id_perfil: int) -> Perfil | None:
        """
        Obtiene un perfil existente por su ID.

        :param id_perfil: ID del perfil
        :return: Perfil encontrado o None
        :raises ValueError: si el ID es inválido
        """
        if id_perfil <= 0:
            raise ValueError("ID de perfil inválido")

        session = Session()
        perfil = session.query(Perfil).filter_by(idPerfil=id_perfil).first()
        session.close()
        return perfil
    def crear_materia(self, nombre: str, descripcion: str) -> bool:
        session = Session()
        # Creamos la materia con un color por defecto ("#FFFFFF") 
        # porque el modelo dice que no puede ser nulo.
        nueva_materia = Materia(nombre=nombre, color="#FFFFFF") 
        session.add(nueva_materia)
        session.commit()
        session.close()
        return True
