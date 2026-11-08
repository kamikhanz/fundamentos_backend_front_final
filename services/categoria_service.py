from fastapi import HTTPException
from sqlmodel import select

from models.categoria import Categoria
from models.producto import Producto
from schemas.categoria import CategoriaCreate, CategoriaUpdate


def obtener_categorias(session):
    return session.exec(select(Categoria)).all()


def obtener_categoria(id: int, session):
    categoria = session.get(Categoria, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def validar_nombre_libre(nombre: str, session, id_actual: int | None = None):
    otra = session.exec(select(Categoria).where(Categoria.nombre == nombre)).first()
    if otra is not None and otra.id != id_actual:
        raise HTTPException(status_code=400, detail="Ya existe esa categoría")


def crear_categoria(data: CategoriaCreate, session):
    validar_nombre_libre(data.nombre, session)
    categoria = Categoria(**data.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def actualizar_categoria(id: int, data: CategoriaUpdate, session):
    categoria = obtener_categoria(id, session)
    if data.nombre is not None:
        validar_nombre_libre(data.nombre, session, id)
    categoria.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def eliminar_categoria(id: int, session):
    categoria = obtener_categoria(id, session)
    producto = session.exec(select(Producto).where(Producto.categoria_id == id)).first()
    if producto is not None:
        raise HTTPException(
            status_code=400, detail="No se puede eliminar: la categoría tiene productos"
        )
    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente"}


def obtener_productos_de_categoria(id: int, session):
    return obtener_categoria(id, session).productos
