from sqlmodel import Session, select
from models.tag import Tag, TagCreate, TagUpdate
from typing import Optional
from datetime import datetime


class TagService:
    """Business logic for Tag model"""
    
    @staticmethod
    def validate_tag(data: TagCreate, session: Session) -> None:
        """Validation rules for tag creation"""
        if len(data.name) < 2:
            raise ValueError("Tag name must be at least 2 characters")
        
        # Check uniqueness
        existing = session.exec(select(Tag).where(Tag.name == data.name)).first()
        if existing:
            raise ValueError("Tag name already exists")
        
        # Validate color format (simple hex check)
        if data.color and not data.color.startswith("#"):
            raise ValueError("Color must be in hex format (e.g., #3b82f6)")
    
    @staticmethod
    def validate_update(tag_id: int, data: TagUpdate, session: Session) -> None:
        """Validation rules for tag update"""
        if data.name:
            existing = session.exec(
                select(Tag).where(Tag.name == data.name, Tag.id != tag_id)
            ).first()
            if existing:
                raise ValueError("Tag name already in use")
        
        if data.color and not data.color.startswith("#"):
            raise ValueError("Color must be in hex format")
    
    @staticmethod
    def before_create(data: TagCreate, session: Session) -> dict:
        """Hook: before creating tag"""
        TagService.validate_tag(data, session)
        return data.model_dump()
    
    @staticmethod
    def after_create(tag: Tag, session: Session):
        """Hook: after creating tag"""
        from services.user_service import AuditService
        AuditService.log("tag_created", tag.id, f"Name: {tag.name}")
    
    @staticmethod
    def before_update(tag_id: int, data: TagUpdate, session: Session) -> dict:
        """Hook: before updating tag"""
        TagService.validate_update(tag_id, data, session)
        return data.model_dump(exclude_unset=True)
    
    @staticmethod
    def after_update(tag: Tag, session: Session):
        """Hook: after updating tag"""
        from services.user_service import AuditService
        AuditService.log("tag_updated", tag.id, f"Name: {tag.name}")
    
    @staticmethod
    def before_delete(tag: Tag, session: Session):
        """Hook: before deleting tag"""
        # Tags can be deleted even if associated with projects (many-to-many)
        pass
    
    @staticmethod
    def after_delete(tag_id: int, session: Session):
        """Hook: after deleting tag"""
        from services.user_service import AuditService
        AuditService.log("tag_deleted", tag_id)
    
    @staticmethod
    def enrich(tag: Tag, session: Session) -> Tag:
        """Add computed fields"""
        tag.project_count = len(tag.projects) if tag.projects else 0
        return tag
