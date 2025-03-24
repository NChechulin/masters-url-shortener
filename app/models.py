from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())


class Link(Base):
    __tablename__ = "links"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, index=True, nullable=False)
    alias = Column(String(50), unique=True, index=True, nullable=True)
    original_url = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)
    last_access = Column(DateTime(timezone=True), nullable=True)
    expiration = Column(DateTime(timezone=True), nullable=True)
