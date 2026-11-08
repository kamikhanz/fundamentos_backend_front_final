from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def crear_token(data: dict):
    contenido = data.copy()

    expiracion = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    contenido.update({"exp": expiracion})

    return jwt.encode(contenido, SECRET_KEY, algorithm=ALGORITHM)
