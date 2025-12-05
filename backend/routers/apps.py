"""
App Builder Router - Manage applications
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import (
    App, AppCreate, AppUpdate, AppRead, PublishStatus,
    Page, FormSchema, DashboardConfig, APIEndpoint, MenuConfig
)
from datetime import datetime

router = APIRouter(prefix="/apps", tags=["apps"])


@router.post("/", response_model=AppRead)
def create_app(app: AppCreate, session: Session = Depends(get_session)):
    """Create a new application"""
    try:
        # Check if app name already exists
        existing = session.exec(select(App).where(App.name == app.name)).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"App '{app.name}' already exists")
        
        db_app = App(**app.model_dump())
        session.add(db_app)
        session.commit()
        session.refresh(db_app)
        
        return AppRead(**db_app.model_dump(), table_count=0)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AppRead])
def list_apps(
    session: Session = Depends(get_session),
    is_active: bool = Query(default=None)
):
    """List all applications"""
    query = select(App)
    
    if is_active is not None:
        query = query.where(App.is_active == is_active)
    
    apps = session.exec(query).all()
    
    # Add counts
    result = []
    for app in apps:
        result.append(AppRead(
            **app.model_dump(),
            table_count=len(app.tables) if app.tables else 0,
            page_count=len(app.pages) if app.pages else 0,
            form_count=len(app.forms) if app.forms else 0,
            dashboard_count=len(app.dashboards) if app.dashboards else 0,
            api_count=len(app.api_endpoints) if app.api_endpoints else 0,
            menu_count=len(app.menus) if app.menus else 0
        ))
    
    return result


@router.get("/{app_id}", response_model=AppRead)
def get_app(app_id: int, session: Session = Depends(get_session)):
    """Get a specific application"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail=f"App with id {app_id} not found")
    
    return AppRead(
        **app.model_dump(),
        table_count=len(app.tables) if app.tables else 0,
        page_count=len(app.pages) if app.pages else 0,
        form_count=len(app.forms) if app.forms else 0,
        dashboard_count=len(app.dashboards) if app.dashboards else 0,
        api_count=len(app.api_endpoints) if app.api_endpoints else 0,
        menu_count=len(app.menus) if app.menus else 0
    )


@router.put("/{app_id}", response_model=AppRead)
def update_app(
    app_id: int,
    app_update: AppUpdate,
    session: Session = Depends(get_session)
):
    """Update an application"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail=f"App with id {app_id} not found")
    
    update_dict = app_update.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(app, key, value)
    
    app.updated_at = datetime.utcnow()
    session.add(app)
    session.commit()
    session.refresh(app)
    
    return AppRead(
        **app.model_dump(),
        table_count=len(app.tables) if app.tables else 0,
        page_count=len(app.pages) if app.pages else 0,
        form_count=len(app.forms) if app.forms else 0,
        dashboard_count=len(app.dashboards) if app.dashboards else 0,
        api_count=len(app.api_endpoints) if app.api_endpoints else 0,
        menu_count=len(app.menus) if app.menus else 0
    )


@router.post("/{app_id}/publish", response_model=AppRead)
def publish_app(app_id: int, session: Session = Depends(get_session)):
    """Publish an application"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail=f"App with id {app_id} not found")
    
    # Update publish status
    app.publish_status = PublishStatus.PUBLISHED
    app.published_at = datetime.utcnow()
    app.version += 1
    app.updated_at = datetime.utcnow()
    
    session.add(app)
    session.commit()
    session.refresh(app)
    
    return AppRead(
        **app.model_dump(),
        table_count=len(app.tables) if app.tables else 0,
        page_count=len(app.pages) if app.pages else 0,
        form_count=len(app.forms) if app.forms else 0,
        dashboard_count=len(app.dashboards) if app.dashboards else 0,
        api_count=len(app.api_endpoints) if app.api_endpoints else 0,
        menu_count=len(app.menus) if app.menus else 0
    )


@router.post("/{app_id}/unpublish", response_model=AppRead)
def unpublish_app(app_id: int, session: Session = Depends(get_session)):
    """Unpublish an application"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail=f"App with id {app_id} not found")
    
    # Update publish status
    app.publish_status = PublishStatus.UNPUBLISHED
    app.updated_at = datetime.utcnow()
    
    session.add(app)
    session.commit()
    session.refresh(app)
    
    return AppRead(
        **app.model_dump(),
        table_count=len(app.tables) if app.tables else 0,
        page_count=len(app.pages) if app.pages else 0,
        form_count=len(app.forms) if app.forms else 0,
        dashboard_count=len(app.dashboards) if app.dashboards else 0,
        api_count=len(app.api_endpoints) if app.api_endpoints else 0,
        menu_count=len(app.menus) if app.menus else 0
    )


@router.delete("/{app_id}")
def delete_app(app_id: int, session: Session = Depends(get_session)):
    """Delete an application and all its tables"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail=f"App with id {app_id} not found")
    
    # Check if app has tables
    if app.tables:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete app with {len(app.tables)} tables. Delete tables first."
        )
    
    session.delete(app)
    session.commit()
    
    return {"message": f"App '{app.name}' deleted successfully"}
