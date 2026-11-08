from fastapi import APIRouter, status

from db.database import SessionDep
from dependencies.auth import AdminUser, CurrentUser
from schemas.pedido import EstadoUpdate, PedidoRead
from services import pedido_service

router = APIRouter(tags=["pedidos"], prefix="/pedidos")


@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_pedido(current_user: CurrentUser, session: SessionDep):
    return pedido_service.crear_pedido(current_user.id, session)


@router.get("/mis-pedidos", response_model=list[PedidoRead])
def get_mis_pedidos(current_user: CurrentUser, session: SessionDep):
    return pedido_service.obtener_mis_pedidos(current_user.id, session)


@router.get("/admin/todos", response_model=list[PedidoRead])
def get_todos(admin: AdminUser, session: SessionDep):
    return pedido_service.obtener_todos(session)


@router.get("/{id}", response_model=PedidoRead)
def get_pedido(id: int, current_user: CurrentUser, session: SessionDep):
    return pedido_service.obtener_pedido(id, current_user, session)


@router.put("/{id}/estado", response_model=PedidoRead)
def update_estado(
    id: int, data: EstadoUpdate, admin: AdminUser, session: SessionDep
):
    return pedido_service.cambiar_estado(id, data.estado, session)
