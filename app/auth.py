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

def get_password_hash(password: str) -> str:
    #Limita a senha a 72 bytes para evitar erro do bcrypt
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
