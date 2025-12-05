from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str
    role: str = Field(default="user")  # admin, user, viewer
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_count: Optional[int] = None
