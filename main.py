from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.auth_controller import router as auth_router
from controller.carrito_controller import router as carrito_router
from controller.categoria_controller import router as categoria_router
from controller.pedido_controller import router as pedido_router
from controller.producto_controller import router as producto_router
from db.database import crear_tablas

app = FastAPI(title="Tienda de motos", lifespan=crear_tablas)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(carrito_router)
app.include_router(pedido_router)
