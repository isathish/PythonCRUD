"""
Dashboards Router - Manage dashboard configurations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import DashboardConfig, DashboardConfigCreate, DashboardConfigUpdate, DashboardConfigRead, App

router = APIRouter(prefix="/apps/{app_id}/dashboards", tags=["dashboards"])


@router.get("", response_model=List[DashboardConfigRead])
def list_dashboards(
    app_id: int,
    session: Session = Depends(get_session)
):
    """List all dashboards for an app"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(DashboardConfig).where(DashboardConfig.app_id == app_id)
    dashboards = session.exec(statement).all()
    return dashboards


@router.post("", response_model=DashboardConfigRead, status_code=201)
def create_dashboard(
    app_id: int,
    dashboard: DashboardConfigCreate,
    session: Session = Depends(get_session)
):
    """Create a new dashboard"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    existing = session.exec(
        select(DashboardConfig).where(DashboardConfig.app_id == app_id, DashboardConfig.name == dashboard.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Dashboard with this name already exists")
    
    db_dashboard = DashboardConfig(**dashboard.model_dump(), app_id=app_id)
    session.add(db_dashboard)
    session.commit()
    session.refresh(db_dashboard)
    return db_dashboard


@router.get("/{dashboard_id}", response_model=DashboardConfigRead)
def get_dashboard(
    app_id: int,
    dashboard_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific dashboard"""
    dashboard = session.get(DashboardConfig, dashboard_id)
    if not dashboard or dashboard.app_id != app_id:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard


@router.patch("/{dashboard_id}", response_model=DashboardConfigRead)
def update_dashboard(
    app_id: int,
    dashboard_id: int,
    dashboard_update: DashboardConfigUpdate,
    session: Session = Depends(get_session)
):
    """Update a dashboard"""
    dashboard = session.get(DashboardConfig, dashboard_id)
    if not dashboard or dashboard.app_id != app_id:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    update_data = dashboard_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dashboard, key, value)
    
    session.add(dashboard)
    session.commit()
    session.refresh(dashboard)
    return dashboard


@router.delete("/{dashboard_id}", status_code=204)
def delete_dashboard(
    app_id: int,
    dashboard_id: int,
    session: Session = Depends(get_session)
):
    """Delete a dashboard"""
    dashboard = session.get(DashboardConfig, dashboard_id)
    if not dashboard or dashboard.app_id != app_id:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    session.delete(dashboard)
    session.commit()
    return None
