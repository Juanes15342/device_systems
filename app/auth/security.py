from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT — se leen del .env
SECRET_KEY = os.getenv("SECRET_KEY", "clave_temporal_cambiar_en_produccion")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def get_password_hash(password: str) -> str:
    """Convierte una contraseña en texto plano a un hash seguro."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano contra su hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token JWT con los datos proporcionados y una fecha de expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica y valida un token JWT. Retorna None si es inválido o expiró."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None