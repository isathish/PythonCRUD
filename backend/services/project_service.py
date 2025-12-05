from sqlmodel import Session, select
from models.project import Project, ProjectCreate, ProjectUpdate, ProjectTagLink
from models.tag import Tag
from typing import Optional
from datetime import datetime, date


class ProjectService:
    """Business logic for Project model"""
    
    @staticmethod
    def validate_project(data: ProjectCreate, session: Session) -> None:
        """Validation rules for project creation"""
        if len(data.name) < 3:
            raise ValueError("Project name must be at least 3 characters")
        
        if data.priority < 1 or data.priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        
        # Validate status
        valid_statuses = ["open", "in_progress", "completed", "archived"]
        if data.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        # Validate dates
        if data.start_date and data.end_date:
            if data.end_date < data.start_date:
                raise ValueError("End date cannot be before start date")
        
        # Validate budget
        if data.budget is not None and data.budget < 0:
            raise ValueError("Budget cannot be negative")
    
    @staticmethod
    def validate_update(project_id: int, data: ProjectUpdate, session: Session) -> None:
        """Validation rules for project update"""
        if data.priority is not None and (data.priority < 1 or data.priority > 5):
            raise ValueError("Priority must be between 1 and 5")
        
        if data.status:
            valid_statuses = ["open", "in_progress", "completed", "archived"]
            if data.status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        if data.budget is not None and data.budget < 0:
            raise ValueError("Budget cannot be negative")
    
    @staticmethod
    def before_create(data: ProjectCreate, session: Session) -> dict:
        """Hook: before creating project"""
        ProjectService.validate_project(data, session)
        
        # Extract tag_ids for separate handling
        create_data = data.model_dump(exclude={"tag_ids"})
        return create_data
    
    @staticmethod
    def after_create(project: Project, session: Session, tag_ids: Optional[list] = None):
        """Hook: after creating project"""
        from services.user_service import AuditService
        from models.project import ProjectTagLink
        
        # Handle tags
        if tag_ids:
            for tag_id in tag_ids:
                tag = session.get(Tag, tag_id)
                if tag:
                    link = ProjectTagLink(project_id=project.id, tag_id=tag_id)
                    session.add(link)
            session.commit()
        
        AuditService.log("project_created", project.id, f"Name: {project.name}")
    
    @staticmethod
    def before_update(project_id: int, data: ProjectUpdate, session: Session) -> dict:
        """Hook: before updating project"""
        ProjectService.validate_update(project_id, data, session)
        
        update_data = data.model_dump(exclude_unset=True, exclude={"tag_ids"})
        update_data["updated_at"] = datetime.utcnow()
        
        return update_data
    
    @staticmethod
    def after_update(project: Project, session: Session, tag_ids: Optional[list] = None):
        """Hook: after updating project"""
        from services.user_service import AuditService
        from models.project import ProjectTagLink
        from sqlmodel import delete
        
        # Handle tags update if provided
        if tag_ids is not None:
            # Clear existing tags
            session.exec(delete(ProjectTagLink).where(ProjectTagLink.project_id == project.id))
            session.commit()
            
            # Add new tags
            for tag_id in tag_ids:
                tag = session.get(Tag, tag_id)
                if tag:
                    link = ProjectTagLink(project_id=project.id, tag_id=tag_id)
                    session.add(link)
            session.commit()
        
        AuditService.log("project_updated", project.id, f"Name: {project.name}")
    
    @staticmethod
    def before_delete(project: Project, session: Session):
        """Hook: before deleting project"""
        # Can add validation here if needed
        pass
    
    @staticmethod
    def after_delete(project_id: int, session: Session):
        """Hook: after deleting project"""
        from services.user_service import AuditService
        AuditService.log("project_deleted", project_id)
    
    @staticmethod
    def enrich(project: Project, session: Session) -> Project:
        """Add computed fields"""
        project.total_tags = len(project.tag_links) if project.tag_links else 0
        
        # Check if overdue
        if project.end_date and project.status not in ["completed", "archived"]:
            project.is_overdue = project.end_date < date.today()
        else:
            project.is_overdue = False
        
        return project
