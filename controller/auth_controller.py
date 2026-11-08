from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import crear_token
from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.usuario import Token, UsuarioCreate, UsuarioRead
from services import usuario_service

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/register", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED
)
def registrar(data: UsuarioCreate, session: SessionDep):
    usuario = usuario_service.registrar_usuario(data, session)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado"
        )

    return usuario


# En el formulario de OAuth2 el campo username lleva el correo
@router.post("/login", response_model=Token)
def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    usuario = usuario_service.autenticar_usuario(data.username, data.password, session)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioRead)
def obtener_mi_usuario(current_user: CurrentUser):
    return current_user
