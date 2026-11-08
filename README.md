# Moto Tienda - Proyecto final

Tienda virtual Full Stack con FastAPI, SQLModel, SQLite y un frontend en HTML, CSS y JavaScript.

La API queda en http://localhost:8000 y la documentacion en http://localhost:8000/docs.

Para el frontend, abrir la carpeta `frontend` en VS Code y usar Live Server en el puerto 5500.
Se abre la carpeta `frontend` y no la del proyecto para que Live Server no recargue la pagina cada vez que cambia `tienda.db`.

## Usuario administrador

La base de datos `tienda.db` ya viene con los productos, las categorias y esta cuenta de prueba:

- Correo: `admin@tienda.com`
- Contraseña: `admin12345`

Los demas usuarios se registran desde la pagina y quedan como clientes.

## Organizacion

| Carpeta            | Contenido                                                             |
| ------------------ | --------------------------------------------------------------------- |
| `frontend/Assets/` | Imagenes de los productos, por categoria. En SQLite se guarda su ruta |
| `core/`            | Configuracion y seguridad (hash y JWT)                                |
| `db/`              | Conexion a SQLite y sesion                                            |
| `models/`          | Tablas de SQLModel                                                    |
| `schemas/`         | Datos de entrada y salida                                             |
| `services/`        | Logica de la aplicacion                                               |
| `controller/`      | Endpoints                                                             |
| `dependencies/`    | Autenticacion y permisos                                              |
| `frontend/`        | Paginas, estilos y JavaScript                                         |
