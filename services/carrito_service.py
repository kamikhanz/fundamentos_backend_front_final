from fastapi import HTTPException
from sqlmodel import select

from models.carrito import Carrito, CarritoItem
from models.producto import Producto
from schemas.carrito import ItemActualizar, ItemAgregar


def obtener_o_crear_carrito(usuario_id: int, session):
    carrito = session.exec(
        select(Carrito).where(Carrito.usuario_id == usuario_id)
    ).first()

    if carrito is None:
        carrito = Carrito(usuario_id=usuario_id)
        session.add(carrito)
        session.commit()
        session.refresh(carrito)

    return carrito


def armar_respuesta(carrito: Carrito):
    items = []
    total = 0

    for item in carrito.items:
        subtotal = round(item.producto.precio * item.cantidad, 2)
        total = total + subtotal
        items.append(
            {
                "id": item.id,
                "producto": item.producto,
                "cantidad": item.cantidad,
                "subtotal": subtotal,
            }
        )

    return {"id": carrito.id, "items": items, "total": round(total, 2)}


def validar_stock(producto: Producto, cantidad: int):
    if cantidad > producto.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente de {producto.nombre}. Disponible: {producto.stock}",
        )


def buscar_item(item_id: int, carrito_id: int, session):
    item = session.exec(
        select(CarritoItem).where(
            CarritoItem.id == item_id, CarritoItem.carrito_id == carrito_id
        )
    ).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Producto no está en el carrito")

    return item


def ver_carrito(usuario_id: int, session):
    return armar_respuesta(obtener_o_crear_carrito(usuario_id, session))


def agregar_item(data: ItemAgregar, usuario_id: int, session):
    producto = session.get(Producto, data.producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    carrito = obtener_o_crear_carrito(usuario_id, session)

    item = session.exec(
        select(CarritoItem).where(
            CarritoItem.carrito_id == carrito.id,
            CarritoItem.producto_id == data.producto_id,
        )
    ).first()

    if item is None:
        validar_stock(producto, data.cantidad)
        item = CarritoItem(
            carrito_id=carrito.id, producto_id=data.producto_id, cantidad=data.cantidad
        )
    else:
        validar_stock(producto, item.cantidad + data.cantidad)
        item.cantidad = item.cantidad + data.cantidad

    session.add(item)
    session.commit()
    session.refresh(carrito)
    return armar_respuesta(carrito)


def actualizar_item(item_id: int, data: ItemActualizar, usuario_id: int, session):
    carrito = obtener_o_crear_carrito(usuario_id, session)
    item = buscar_item(item_id, carrito.id, session)

    validar_stock(item.producto, data.cantidad)
    item.cantidad = data.cantidad

    session.add(item)
    session.commit()
    session.refresh(carrito)
    return armar_respuesta(carrito)


def eliminar_item(item_id: int, usuario_id: int, session):
    carrito = obtener_o_crear_carrito(usuario_id, session)
    item = buscar_item(item_id, carrito.id, session)

    session.delete(item)
    session.commit()
    session.refresh(carrito)
    return armar_respuesta(carrito)
