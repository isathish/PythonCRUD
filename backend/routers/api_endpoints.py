"""
API Endpoints Router - Manage custom API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import APIEndpoint, APIEndpointCreate, APIEndpointUpdate, APIEndpointRead, App

router = APIRouter(prefix="/apps/{app_id}/api-endpoints", tags=["api-endpoints"])


@router.get("", response_model=List[APIEndpointRead])
def list_api_endpoints(
    app_id: int,
    session: Session = Depends(get_session)
):
    """List all API endpoints for an app"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(APIEndpoint).where(APIEndpoint.app_id == app_id)
    endpoints = session.exec(statement).all()
    return endpoints


@router.post("", response_model=APIEndpointRead, status_code=201)
def create_api_endpoint(
    app_id: int,
    endpoint: APIEndpointCreate,
    session: Session = Depends(get_session)
):
    """Create a new API endpoint"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    existing = session.exec(
        select(APIEndpoint).where(
            APIEndpoint.app_id == app_id,
            APIEndpoint.path == endpoint.path,
            APIEndpoint.method == endpoint.method
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="API endpoint with this path and method already exists")
    
    db_endpoint = APIEndpoint(**endpoint.model_dump(), app_id=app_id)
    session.add(db_endpoint)
    session.commit()
    session.refresh(db_endpoint)
    return db_endpoint


@router.get("/{endpoint_id}", response_model=APIEndpointRead)
def get_api_endpoint(
    app_id: int,
    endpoint_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific API endpoint"""
    endpoint = session.get(APIEndpoint, endpoint_id)
    if not endpoint or endpoint.app_id != app_id:
        raise HTTPException(status_code=404, detail="API endpoint not found")
    return endpoint


@router.patch("/{endpoint_id}", response_model=APIEndpointRead)
def update_api_endpoint(
    app_id: int,
    endpoint_id: int,
    endpoint_update: APIEndpointUpdate,
    session: Session = Depends(get_session)
):
    """Update an API endpoint"""
    endpoint = session.get(APIEndpoint, endpoint_id)
    if not endpoint or endpoint.app_id != app_id:
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    update_data = endpoint_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(endpoint, key, value)
    
    session.add(endpoint)
    session.commit()
    session.refresh(endpoint)
    return endpoint


@router.delete("/{endpoint_id}", status_code=204)
def delete_api_endpoint(
    app_id: int,
    endpoint_id: int,
    session: Session = Depends(get_session)
):
    """Delete an API endpoint"""
    endpoint = session.get(APIEndpoint, endpoint_id)
    if not endpoint or endpoint.app_id != app_id:
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    session.delete(endpoint)
    session.commit()
    return None
