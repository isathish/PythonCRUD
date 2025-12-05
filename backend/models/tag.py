from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.project import Project, ProjectTagLink


class TagBase(SQLModel):
    name: str = Field(unique=True, index=True)
    color: str = Field(default="#3b82f6")
    description: Optional[str] = None


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - many-to-many through ProjectTagLink
    project_links: List["ProjectTagLink"] = Relationship(back_populates="tag")


class TagCreate(TagBase):
    pass


class TagUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


class TagRead(TagBase):
    id: int
    created_at: datetime
    project_count: Optional[int] = None
