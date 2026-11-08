from fastapi import APIRouter, Query, status

from db.database import SessionDep
from dependencies.auth import AdminUser
from schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from services import producto_service

router = APIRouter(tags=["productos"], prefix="/productos")


@router.get("/", response_model=list[ProductoRead])
def get_productos(
    session: SessionDep, buscar: str | None = None, categoria_id: int | None = None
):
    return producto_service.obtener_productos(session, buscar, categoria_id)


# Estas dos van antes de /{id} para que FastAPI no las confunda con un id
@router.get("/aleatorios", response_model=list[ProductoRead])
def get_aleatorios(session: SessionDep, limite: int = Query(default=8, ge=1, le=50)):
    return producto_service.obtener_aleatorios(session, limite)


@router.get("/destacados", response_model=list[ProductoRead])
def get_destacados(session: SessionDep):
    return producto_service.obtener_destacados(session)


@router.get("/{id}", response_model=ProductoRead)
def get_producto(id: int, session: SessionDep):
    return producto_service.obtener_producto(id, session)


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, admin: AdminUser, session: SessionDep):
    return producto_service.crear_producto(data, session)


@router.put("/{id}", response_model=ProductoRead)
def update_producto(
    id: int, data: ProductoUpdate, admin: AdminUser, session: SessionDep
):
    return producto_service.actualizar_producto(id, data, session)


@router.delete("/{id}")
def delete_producto(id: int, admin: AdminUser, session: SessionDep):
    return producto_service.eliminar_producto(id, session)
