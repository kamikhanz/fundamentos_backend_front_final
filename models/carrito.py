from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.producto import Producto
    from models.usuario import Usuario


class Carrito(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", unique=True)

    usuario: Optional["Usuario"] = Relationship(back_populates="carrito")
    items: list["CarritoItem"] = Relationship(back_populates="carrito")


class CarritoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    carrito_id: int = Field(foreign_key="carrito.id", index=True)
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int

    carrito: Optional["Carrito"] = Relationship(back_populates="items")
    producto: Optional["Producto"] = Relationship()
