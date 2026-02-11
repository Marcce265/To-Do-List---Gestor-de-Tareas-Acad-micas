# Arquitectura del Proyecto

El proyecto sigue una arquitectura en capas separando responsabilidades:

- *Modelo (modelo/):* Define las entidades y configuración de base de datos usando SQLAlchemy.
- *Lógica (logica/):* Implementa las operaciones CRUD y reglas de negocio.
- *Presentación (main.py):* Punto de entrada del sistema.
- *Tests (tests/):* Pruebas unitarias con pytest.

## Patrón aplicado

Se utiliza una arquitectura tipo MVC simplificada:

- Model → modelo/
- Controller/Service → logica/
- View → Interfaz por consola (main.py)