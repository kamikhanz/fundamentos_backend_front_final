from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from core.config import ALGORITHM, SECRET_KEY
from db.database import SessionDep
from models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la autenticación",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        if email is None:
            raise error

    except jwt.InvalidTokenError:
        raise error

    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()

    if usuario is None:
        raise error

    return usuario


CurrentUser = Annotated[Usuario, Depends(obtener_usuario_actual)]


def obtener_admin(current_user: CurrentUser):
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede hacer esto",
        )

    return current_user


AdminUser = Annotated[Usuario, Depends(obtener_admin)]
