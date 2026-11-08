from fastapi import HTTPException
from sqlmodel import col, select

from models.pedido import Pedido, PedidoItem
from models.usuario import Usuario
from services.carrito_service import obtener_o_crear_carrito, validar_stock

ESTADOS = ["pendiente", "procesando", "enviado", "entregado"]


def crear_pedido(usuario_id: int, session):
    carrito = obtener_o_crear_carrito(usuario_id, session)

    if len(carrito.items) == 0:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    # Primero se valida todo, asi no queda una compra a medias
    total = 0
    for item in carrito.items:
        validar_stock(item.producto, item.cantidad)
        total = total + item.producto.precio * item.cantidad

    pedido = Pedido(usuario_id=usuario_id, total=round(total, 2))

    for item in list(carrito.items):
        pedido.items.append(
            PedidoItem(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
            )
        )
        item.producto.stock = item.producto.stock - item.cantidad
        session.add(item.producto)
        session.delete(item)

    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido


def obtener_mis_pedidos(usuario_id: int, session):
    return session.exec(
        select(Pedido)
        .where(Pedido.usuario_id == usuario_id)
        .order_by(col(Pedido.id).desc())
    ).all()


def obtener_pedido(id: int, usuario: Usuario, session):
    pedido = session.get(Pedido, id)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if pedido.usuario_id != usuario.id and usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Este pedido no es tuyo")

    return pedido


def obtener_todos(session):
    return session.exec(select(Pedido).order_by(col(Pedido.id).desc())).all()


def cambiar_estado(id: int, estado: str, session):
    if estado not in ESTADOS:
        raise HTTPException(status_code=400, detail="Estado no válido")

    pedido = session.get(Pedido, id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    pedido.estado = estado
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido
