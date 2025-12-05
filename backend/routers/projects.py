from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from core.database import get_session
from models.project import Project, ProjectCreate, ProjectUpdate, ProjectRead
from services.project_service import ProjectService
from services.filter_engine import QueryBuilder

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead)
def create_project(project: ProjectCreate, session: Session = Depends(get_session)):
    """Create a new project with business logic validation"""
    try:
        # Business logic: validation and pre-create hook
        tag_ids = project.tag_ids
        project_data = ProjectService.before_create(project, session)
        
        db_project = Project(**project_data)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        
        # Business logic: post-create hook (handles tags)
        ProjectService.after_create(db_project, session, tag_ids)
        session.refresh(db_project)
        
        # Enrich with computed fields
        db_project = ProjectService.enrich(db_project, session)
        
        return ProjectRead.from_orm_with_tags(db_project, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Dict[str, Any])
def list_projects(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None, description="Sort format: field:asc,field:desc"),
    # Simple filters
    name__ilike: Optional[str] = None,
    status__eq: Optional[str] = None,
    status__in: Optional[str] = None,
    priority__gte: Optional[int] = None,
    priority__lte: Optional[int] = None,
    budget__gte: Optional[float] = None,
    budget__lte: Optional[float] = None,
    owner_id__eq: Optional[int] = None,
):
    """List projects with advanced filtering, sorting, and pagination"""
    
    # Build filters dict
    filters = {}
    if name__ilike:
        filters["name__ilike"] = name__ilike
    if status__eq:
        filters["status__eq"] = status__eq
    if status__in:
        filters["status__in"] = status__in
    if priority__gte is not None:
        filters["priority__gte"] = priority__gte
    if priority__lte is not None:
        filters["priority__lte"] = priority__lte
    if budget__gte is not None:
        filters["budget__gte"] = budget__gte
    if budget__lte is not None:
        filters["budget__lte"] = budget__lte
    if owner_id__eq is not None:
        filters["owner_id__eq"] = owner_id__eq
    
    # Build query
    query = select(Project)
    
    # Apply filters
    if filters:
        query = QueryBuilder.apply_simple_filters(query, Project, filters)
    
    # Apply sorting
    if sort:
        query = QueryBuilder.apply_sorting(query, Project, sort)
    
    # Get total count
    total = QueryBuilder.get_total_count(session, query)
    
    # Apply pagination
    query = QueryBuilder.apply_pagination(query, page, limit)
    
    projects = session.exec(query).all()
    
    # Enrich with computed fields
    enriched_projects = [ProjectService.enrich(project, session) for project in projects]
    
    return {
        "data": enriched_projects,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.post("/filter", response_model=Dict[str, Any])
def filter_projects(
    filter_json: Dict[str, Any] = Body(...),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    """
    Filter projects with complex JSON filters (AND/OR logic).
    
    Example payload:
    {
        "logic": "and",
        "filters": [
            {"field": "status", "op": "eq", "value": "active"},
            {
                "logic": "or",
                "filters": [
                    {"field": "priority", "op": "gte", "value": 3},
                    {"field": "name", "op": "ilike", "value": "critical"}
                ]
            }
        ]
    }
    """
    # Build query
    query = select(Project)
    
    # Apply JSON filters
    query = QueryBuilder.apply_json_filters(query, Project, filter_json)
    
    # Apply sorting
    if sort:
        query = QueryBuilder.apply_sorting(query, Project, sort)
    
    # Get total count
    total = QueryBuilder.get_total_count(session, query)
    
    # Apply pagination
    query = QueryBuilder.apply_pagination(query, page, limit)
    
    projects = session.exec(query).all()
    
    # Enrich with computed fields
    enriched_projects = [ProjectService.enrich(project, session) for project in projects]
    
    return {
        "data": enriched_projects,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session)):
    """Get a specific project by ID"""
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Enrich with computed fields
    project = ProjectService.enrich(project, session)
    
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, project: ProjectUpdate, session: Session = Depends(get_session)):
    """Update a project with business logic validation"""
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Business logic: validation and pre-update hook
        tag_ids = project.tag_ids if hasattr(project, 'tag_ids') else None
        update_data = ProjectService.before_update(project_id, project, session)
        
        for key, value in update_data.items():
            setattr(db_project, key, value)
        
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        
        # Business logic: post-update hook (handles tags)
        ProjectService.after_update(db_project, session, tag_ids)
        session.refresh(db_project)
        
        # Enrich with computed fields
        db_project = ProjectService.enrich(db_project, session)
        
        return db_project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    """Delete a project with business logic validation"""
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Business logic: pre-delete hook
        ProjectService.before_delete(project, session)
        
        session.delete(project)
        session.commit()
        
        # Business logic: post-delete hook
        ProjectService.after_delete(project_id, session)
        
        return {"message": "Project deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
