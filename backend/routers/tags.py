from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from core.database import get_session
from models.tag import Tag, TagCreate, TagUpdate, TagRead
from services.tag_service import TagService
from services.filter_engine import QueryBuilder

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagRead)
def create_tag(tag: TagCreate, session: Session = Depends(get_session)):
    """Create a new tag with business logic validation"""
    try:
        # Business logic: validation and pre-create hook
        tag_data = TagService.before_create(tag, session)
        
        db_tag = Tag(**tag_data)
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        
        # Business logic: post-create hook
        TagService.after_create(db_tag, session)
        
        # Enrich with computed fields
        db_tag = TagService.enrich(db_tag, session)
        
        return db_tag
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Dict[str, Any])
def list_tags(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None, description="Sort format: field:asc,field:desc"),
    # Simple filters
    name__ilike: Optional[str] = None,
    color__eq: Optional[str] = None,
):
    """List tags with advanced filtering, sorting, and pagination"""
    
    # Build filters dict
    filters = {}
    if name__ilike:
        filters["name__ilike"] = name__ilike
    if color__eq:
        filters["color__eq"] = color__eq
    
    # Build query
    query = select(Tag)
    
    # Apply filters
    if filters:
        query = QueryBuilder.apply_simple_filters(query, Tag, filters)
    
    # Apply sorting
    if sort:
        query = QueryBuilder.apply_sorting(query, Tag, sort)
    
    # Get total count
    total = QueryBuilder.get_total_count(session, query)
    
    # Apply pagination
    query = QueryBuilder.apply_pagination(query, page, limit)
    
    tags = session.exec(query).all()
    
    # Enrich with computed fields
    enriched_tags = [TagService.enrich(tag, session) for tag in tags]
    
    return {
        "data": enriched_tags,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag_id: int, session: Session = Depends(get_session)):
    """Get a specific tag by ID"""
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Enrich with computed fields
    tag = TagService.enrich(tag, session)
    
    return tag


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(tag_id: int, tag: TagUpdate, session: Session = Depends(get_session)):
    """Update a tag with business logic validation"""
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    try:
        # Business logic: validation and pre-update hook
        update_data = TagService.before_update(tag_id, tag, session)
        
        for key, value in update_data.items():
            setattr(db_tag, key, value)
        
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        
        # Business logic: post-update hook
        TagService.after_update(db_tag, session)
        
        # Enrich with computed fields
        db_tag = TagService.enrich(db_tag, session)
        
        return db_tag
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, session: Session = Depends(get_session)):
    """Delete a tag with business logic validation"""
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    try:
        # Business logic: pre-delete hook
        TagService.before_delete(tag, session)
        
        session.delete(tag)
        session.commit()
        
        # Business logic: post-delete hook
        TagService.after_delete(tag_id, session)
        
        return {"message": "Tag deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
