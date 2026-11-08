from fastapi import APIRouter, status

from db.database import SessionDep
from dependencies.auth import AdminUser
from schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from schemas.producto import ProductoRead
from services import categoria_service

router = APIRouter(tags=["categorias"], prefix="/categorias")


@router.get("/", response_model=list[CategoriaRead])
def get_categorias(session: SessionDep):
    return categoria_service.obtener_categorias(session)


@router.get("/{id}", response_model=CategoriaRead)
def get_categoria(id: int, session: SessionDep):
    return categoria_service.obtener_categoria(id, session)


@router.get("/{id}/productos", response_model=list[ProductoRead])
def get_productos_de_categoria(id: int, session: SessionDep):
    return categoria_service.obtener_productos_de_categoria(id, session)


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def create_categoria(data: CategoriaCreate, admin: AdminUser, session: SessionDep):
    return categoria_service.crear_categoria(data, session)


@router.put("/{id}", response_model=CategoriaRead)
def update_categoria(
    id: int, data: CategoriaUpdate, admin: AdminUser, session: SessionDep
):
    return categoria_service.actualizar_categoria(id, data, session)


@router.delete("/{id}")
def delete_categoria(id: int, admin: AdminUser, session: SessionDep):
    return categoria_service.eliminar_categoria(id, session)
