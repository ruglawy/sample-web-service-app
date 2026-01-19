import uuid
from sqlalchemy import (
    Column, String, Boolean, DateTime,
    ForeignKey, Table
)
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("group_id", String, ForeignKey("groups.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DATETIME, default=datetime.utcnow)
    updated_at = Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)

    groups = relationship(
        "Group",
        secondary=user_groups,
        back_populates="users"
    )

class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups"
    )

