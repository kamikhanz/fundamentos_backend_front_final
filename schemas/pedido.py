from datetime import datetime

from sqlmodel import SQLModel

from schemas.producto import ProductoRead
from schemas.usuario import UsuarioRead


class PedidoItemRead(SQLModel):
    id: int
    producto: ProductoRead
    cantidad: int
    precio_unitario: float


class PedidoRead(SQLModel):
    id: int
    fecha: datetime
    total: float
    estado: str
    usuario: UsuarioRead
    items: list[PedidoItemRead]


class EstadoUpdate(SQLModel):
    estado: str
