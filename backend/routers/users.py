from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from core.database import get_session
from models.user import User, UserCreate, UserUpdate, UserRead
from services.user_service import UserService
from services.filter_engine import QueryBuilder

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user with business logic validation"""
    try:
        # Business logic: validation and pre-create hook
        user_data = UserService.before_create(user, session)
        
        db_user = User(**user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        # Business logic: post-create hook
        UserService.after_create(db_user, session)
        
        # Enrich with computed fields
        db_user = UserService.enrich(db_user, session)
        
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Dict[str, Any])
def list_users(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None, description="Sort format: field:asc,field:desc"),
    # Simple filters
    email__ilike: Optional[str] = None,
    role__eq: Optional[str] = None,
    role__in: Optional[str] = None,
    is_active: Optional[bool] = None,
    full_name__ilike: Optional[str] = None,
):
    """List users with advanced filtering, sorting, and pagination"""
    
    # Build filters dict
    filters = {}
    if email__ilike:
        filters["email__ilike"] = email__ilike
    if role__eq:
        filters["role__eq"] = role__eq
    if role__in:
        filters["role__in"] = role__in
    if is_active is not None:
        filters["is_active__eq"] = is_active
    if full_name__ilike:
        filters["full_name__ilike"] = full_name__ilike
    
    # Build query
    query = select(User)
    
    # Apply filters
    if filters:
        query = QueryBuilder.apply_simple_filters(query, User, filters)
    
    # Apply sorting
    if sort:
        query = QueryBuilder.apply_sorting(query, User, sort)
    
    # Get total count
    total = QueryBuilder.get_total_count(session, query)
    
    # Apply pagination
    query = QueryBuilder.apply_pagination(query, page, limit)
    
    users = session.exec(query).all()
    
    # Enrich with computed fields
    enriched_users = [UserService.enrich(user, session) for user in users]
    
    return {
        "data": enriched_users,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user by ID"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Enrich with computed fields
    user = UserService.enrich(user, session)
    
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    """Update a user with business logic validation"""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Business logic: validation and pre-update hook
        update_data = UserService.before_update(user_id, user, session)
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        # Business logic: post-update hook
        UserService.after_update(db_user, session)
        
        # Enrich with computed fields
        db_user = UserService.enrich(db_user, session)
        
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user with business logic validation"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Business logic: pre-delete hook
        UserService.before_delete(user, session)
        
        session.delete(user)
        session.commit()
        
        # Business logic: post-delete hook
        UserService.after_delete(user_id, session)
        
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
