from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Optional
import os

# carrega SECRET_KEY da variável de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")  # em produção, sempre sobrescrever
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_password(password: str) -> str:
    """Garante que a senha tenha no máximo 72 bytes (limite do bcrypt)."""
    if not isinstance(password, str):
        password = str(password)
    password_bytes = password.encode("utf-8")[:72]
    # Garante que não haverá erro de decode
    return password_bytes.decode("utf-8", errors="ignore")

def get_password_hash(password: str) -> str:
    safe_password = _truncate_password(password)
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = _truncate_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
