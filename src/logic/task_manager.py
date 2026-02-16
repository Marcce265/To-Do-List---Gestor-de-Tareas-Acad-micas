from datetime import date
from typing import Optional
from sqlalchemy.orm import sessionmaker
from src.model.declarative_base import engine
from src.model.modelo import Usuario

Session = sessionmaker(bind=engine)


class TaskManager:

    def crear_usuario(self, nombre: str, correo: str) -> Usuario:
        """
        HU-001: Crea un nuevo usuario.
        
        Args:
            nombre: Nombre del usuario (obligatorio)
            correo: Correo del usuario (obligatorio y único)
        
        Returns:
            Usuario creado y persistido
        
        Raises:
            ValueError: Si nombre o correo están vacíos, o correo duplicado
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        if not correo or not correo.strip():
            raise ValueError("El correo no puede estar vacío")
        
        session = Session()
        try:
            # Validar correo único
            usuario_existente = session.query(Usuario).filter_by(
                correo=correo.strip()
            ).first()
            
            if usuario_existente:
                raise ValueError(f"El correo {correo} ya está registrado")
            
            usuario = Usuario(
                nombre=nombre.strip(),
                correo=correo.strip(),
                fecha_creacion=date.today()
            )
            
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario
        finally:
            session.close()
    def seleccionar_usuario(self, id_usuario: int) -> Optional[Usuario]:
        """
        HU-002: Selecciona un usuario por ID.
        
        Args:
            id_usuario: ID del usuario a buscar
        
        Returns:
            Usuario encontrado o None si no existe
        
        Raises:
            ValueError: Si el ID es inválido (≤ 0)
        """
        """if id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser mayor a 0")
        
        session = Session()
        try:
            usuario = session.query(Usuario).filter_by(
                idUsuario=id_usuario
            ).first()
            return usuario
        finally:
            session.close()"""