from fastapi import HTTPException
from sqlmodel import col, func, or_, select

from models.carrito import CarritoItem
from models.categoria import Categoria
from models.pedido import PedidoItem
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoUpdate


def obtener_productos(session, buscar: str | None, categoria_id: int | None):
    consulta = select(Producto)

    if buscar:
        consulta = consulta.where(
            or_(
                col(Producto.nombre).contains(buscar),
                col(Producto.descripcion).contains(buscar),
            )
        )

    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)

    return session.exec(consulta).all()


def obtener_aleatorios(session, limite: int):
    return session.exec(select(Producto).order_by(func.random()).limit(limite)).all()


def obtener_destacados(session):
    return session.exec(select(Producto).where(Producto.destacado == True)).all()


def obtener_producto(id: int, session):
    producto = session.get(Producto, id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def validar_categoria(categoria_id: int, session):
    if session.get(Categoria, categoria_id) is None:
        raise HTTPException(status_code=400, detail="La categoría no existe")


def crear_producto(data: ProductoCreate, session):
    validar_categoria(data.categoria_id, session)
    producto = Producto(**data.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def actualizar_producto(id: int, data: ProductoUpdate, session):
    producto = obtener_producto(id, session)
    if data.categoria_id is not None:
        validar_categoria(data.categoria_id, session)
    producto.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def eliminar_producto(id: int, session):
    producto = obtener_producto(id, session)

    en_pedido = session.exec(
        select(PedidoItem).where(PedidoItem.producto_id == id)
    ).first()
    if en_pedido is not None:
        raise HTTPException(
            status_code=400, detail="No se puede eliminar: el producto tiene pedidos"
        )

    items = session.exec(select(CarritoItem).where(CarritoItem.producto_id == id)).all()
    for item in items:
        session.delete(item)

    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado correctamente"}
