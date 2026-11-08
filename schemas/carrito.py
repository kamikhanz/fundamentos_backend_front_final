from sqlmodel import Field, SQLModel

from schemas.producto import ProductoRead


class ItemAgregar(SQLModel):
    producto_id: int
    cantidad: int = Field(default=1, gt=0)


class ItemActualizar(SQLModel):
    cantidad: int = Field(gt=0)


class CarritoItemRead(SQLModel):
    id: int
    producto: ProductoRead
    cantidad: int
    subtotal: float


class CarritoRead(SQLModel):
    id: int
    items: list[CarritoItemRead]
    total: float
