from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, auth, logger_config, rate_limiter
from .database import engine, SessionLocal
import os

# cria tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure User API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logger_config.logger

@app.post("/register", status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db), request: Request = None):
    existing = db.query(models.User).filter((models.User.username==user.username) | (models.User.email==user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="username or email already registered")
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"register - username={db_user.username} ip={(request.client.host if request else 'unknown')}")
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

@app.post("/login", response_model=schemas.Token)
def login(payload: dict, db: Session = Depends(get_db), request: Request = None):
    ip = request.client.host if request else "unknown"
    username = payload.get("username")
    password = payload.get("password")
    # IP block check
    if rate_limiter.is_blocked(ip):
        db.add(models.AuthLog(username=username, ip=ip, success=False, reason="blocked"))
        db.commit()
        logger.info(f"blocked_login - username={username} ip={ip}")
        raise HTTPException(status_code=403, detail="Too many attempts. Try later.")
    user = db.query(models.User).filter((models.User.username==username) | (models.User.email==username)).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        rate_limiter.register_attempt(ip)
        db.add(models.AuthLog(username=username, ip=ip, success=False, reason="bad_credentials"))
        db.commit()
        logger.info(f"failed_login - username={username} ip={ip}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # sucesso: reset attempts
    rate_limiter.reset_attempts(ip)
    token = auth.create_access_token({"sub": str(user.id), "username": user.username})
    db.add(models.AuthLog(username=username, ip=ip, success=True, reason="login_ok"))
    db.commit()
    logger.info(f"login_ok - username={username} ip={ip}")
    return {"access_token": token, "token_type": "bearer"}
