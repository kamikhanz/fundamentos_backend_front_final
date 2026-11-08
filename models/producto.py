from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.categoria import Categoria


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150, index=True)
    codigo: str | None = Field(default=None, max_length=30)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float
    stock: int = Field(default=0)
    imagen: str | None = None
    destacado: bool = Field(default=False)
    categoria_id: int = Field(foreign_key="categoria.id", index=True)

    categoria: Optional["Categoria"] = Relationship(back_populates="productos")
