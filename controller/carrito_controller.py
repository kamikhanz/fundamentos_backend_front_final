from fastapi import APIRouter

from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.carrito import CarritoRead, ItemActualizar, ItemAgregar
from services import carrito_service

router = APIRouter(tags=["carrito"], prefix="/carrito")


@router.get("/", response_model=CarritoRead)
def get_carrito(current_user: CurrentUser, session: SessionDep):
    return carrito_service.ver_carrito(current_user.id, session)


@router.post("/items", response_model=CarritoRead)
def add_item(data: ItemAgregar, current_user: CurrentUser, session: SessionDep):
    return carrito_service.agregar_item(data, current_user.id, session)


@router.put("/items/{item_id}", response_model=CarritoRead)
def update_item(
    item_id: int, data: ItemActualizar, current_user: CurrentUser, session: SessionDep
):
    return carrito_service.actualizar_item(item_id, data, current_user.id, session)


@router.delete("/items/{item_id}", response_model=CarritoRead)
def delete_item(item_id: int, current_user: CurrentUser, session: SessionDep):
    return carrito_service.eliminar_item(item_id, current_user.id, session)
