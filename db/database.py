from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def obtener_sesion():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(obtener_sesion)]
