from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuthLog(Base):
    __tablename__ = "auth_logs"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    ip = Column(String, nullable=True)
    success = Column(Boolean, nullable=False)
    reason = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
