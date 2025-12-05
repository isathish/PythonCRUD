"""
Pages Router - Manage pages within applications
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import Page, PageCreate, PageUpdate, PageRead, App

router = APIRouter(prefix="/apps/{app_id}/pages", tags=["pages"])


@router.get("", response_model=List[PageRead])
def list_pages(
    app_id: int,
    session: Session = Depends(get_session)
):
    """List all pages for an app"""
    # Verify app exists
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(Page).where(Page.app_id == app_id)
    pages = session.exec(statement).all()
    return pages


@router.post("", response_model=PageRead, status_code=201)
def create_page(
    app_id: int,
    page: PageCreate,
    session: Session = Depends(get_session)
):
    """Create a new page"""
    # Verify app exists
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    # Check if page with same name exists
    existing = session.exec(
        select(Page).where(Page.app_id == app_id, Page.name == page.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Page with this name already exists")
    
    db_page = Page(**page.model_dump(), app_id=app_id)
    session.add(db_page)
    session.commit()
    session.refresh(db_page)
    return db_page


@router.get("/{page_id}", response_model=PageRead)
def get_page(
    app_id: int,
    page_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific page"""
    page = session.get(Page, page_id)
    if not page or page.app_id != app_id:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.patch("/{page_id}", response_model=PageRead)
def update_page(
    app_id: int,
    page_id: int,
    page_update: PageUpdate,
    session: Session = Depends(get_session)
):
    """Update a page"""
    page = session.get(Page, page_id)
    if not page or page.app_id != app_id:
        raise HTTPException(status_code=404, detail="Page not found")
    
    update_data = page_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(page, key, value)
    
    session.add(page)
    session.commit()
    session.refresh(page)
    return page


@router.delete("/{page_id}", status_code=204)
def delete_page(
    app_id: int,
    page_id: int,
    session: Session = Depends(get_session)
):
    """Delete a page"""
    page = session.get(Page, page_id)
    if not page or page.app_id != app_id:
        raise HTTPException(status_code=404, detail="Page not found")
    
    session.delete(page)
    session.commit()
    return None
