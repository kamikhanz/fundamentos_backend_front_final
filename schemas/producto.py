from sqlmodel import Field, SQLModel

from schemas.categoria import CategoriaRead


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    codigo: str | None = Field(default=None, max_length=30)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    imagen: str | None = None
    destacado: bool = False
    categoria_id: int


class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    codigo: str | None = Field(default=None, max_length=30)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    imagen: str | None = None
    destacado: bool | None = None
    categoria_id: int | None = None


class ProductoRead(SQLModel):
    id: int
    nombre: str
    codigo: str | None = None
    descripcion: str | None = None
    precio: float
    stock: int
    imagen: str | None = None
    destacado: bool
    categoria_id: int
    categoria: CategoriaRead | None = None
