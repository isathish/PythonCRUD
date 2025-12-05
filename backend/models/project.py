from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date

if TYPE_CHECKING:
    from models.user import User
    from models.tag import Tag


class ProjectTagLink(SQLModel, table=True):
    __tablename__ = "projecttaglink"
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    
    # Relationships to both sides
    project: "Project" = Relationship(back_populates="tag_links")
    tag: "Tag" = Relationship(back_populates="project_links")


class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="open")  # open, in_progress, completed, archived
    priority: int = Field(default=3, ge=1, le=5)  # 1-5
    budget: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    owner_id: int = Field(foreign_key="user.id")


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner: Optional["User"] = Relationship(back_populates="projects")
    tag_links: List["ProjectTagLink"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
    tag_ids: Optional[List[int]] = []


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    budget: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    owner_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_tags: Optional[int] = None
    is_overdue: Optional[bool] = None
    owner: Optional["UserRead"] = None
    tags: List["TagRead"] = []
    
    @classmethod
    def from_orm_with_tags(cls, project: "Project", session):
        """Create ProjectRead with tags loaded from tag_links"""
        from models.tag import TagRead, Tag
        
        # Load tags through the link table
        tags = []
        if hasattr(project, 'tag_links') and project.tag_links:
            for link in project.tag_links:
                if link.tag:
                    tags.append(TagRead.model_validate(link.tag))
        
        # Create dict from project
        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "priority": project.priority,
            "budget": project.budget,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "tags": tags,
        }
        
        # Add computed fields if they exist
        if hasattr(project, 'total_tags'):
            data['total_tags'] = project.total_tags
        if hasattr(project, 'is_overdue'):
            data['is_overdue'] = project.is_overdue
        if hasattr(project, 'owner') and project.owner:
            from models.user import UserRead
            data['owner'] = UserRead.model_validate(project.owner)
            
        return cls(**data)


# Avoid circular imports
from models.user import UserRead
from models.tag import TagRead

ProjectRead.model_rebuild()
