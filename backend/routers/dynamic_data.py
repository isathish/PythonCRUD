"""
Dynamic Data Router - CRUD operations for dynamically created tables
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Dict, Any, List
from core.database import get_session
from models.schema_builder import DynamicData, TableSchema
from services.table_generator_service import DynamicDataService, TableGeneratorService

router = APIRouter(prefix="/data", tags=["dynamic-data"])


@router.post("/{table_name}")
def create_record(
    table_name: str,
    data: Dict[str, Any],
    session: Session = Depends(get_session)
):
    """Create a new record in a dynamic table"""
    # Get table schema
    table_schema = session.exec(
        session.query(TableSchema).filter(TableSchema.name == table_name)
    ).first()
    
    if not table_schema:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    try:
        record = DynamicDataService.create_record(
            table_name, data, table_schema, session
        )
        return {
            "id": record.record_id,
            "table_name": record.table_name,
            "data": record.data,
            "created_at": record.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{table_name}")
def list_records(
    table_name: str,
    session: Session = Depends(get_session),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    """List records from a dynamic table"""
    # Get table schema
    table_schema = session.exec(
        session.query(TableSchema).filter(TableSchema.name == table_name)
    ).first()
    
    if not table_schema:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    records, total = DynamicDataService.get_records(
        table_name, session, page=page, limit=limit
    )
    
    return {
        "data": [
            {
                "id": record.record_id,
                "data": record.data,
                "created_at": record.created_at,
                "updated_at": record.updated_at
            }
            for record in records
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{table_name}/{record_id}")
def get_record(
    table_name: str,
    record_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific record from a dynamic table"""
    record = DynamicDataService.get_record(table_name, record_id, session)
    
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Record with id {record_id} not found in table '{table_name}'"
        )
    
    return {
        "id": record.record_id,
        "table_name": record.table_name,
        "data": record.data,
        "created_at": record.created_at,
        "updated_at": record.updated_at
    }


@router.put("/{table_name}/{record_id}")
def update_record(
    table_name: str,
    record_id: int,
    data: Dict[str, Any],
    session: Session = Depends(get_session)
):
    """Update a record in a dynamic table"""
    # Get table schema
    table_schema = session.exec(
        session.query(TableSchema).filter(TableSchema.name == table_name)
    ).first()
    
    if not table_schema:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    try:
        record = DynamicDataService.update_record(
            table_name, record_id, data, table_schema, session
        )
        return {
            "id": record.record_id,
            "table_name": record.table_name,
            "data": record.data,
            "updated_at": record.updated_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{table_name}/{record_id}")
def delete_record(
    table_name: str,
    record_id: int,
    session: Session = Depends(get_session)
):
    """Delete a record from a dynamic table"""
    try:
        DynamicDataService.delete_record(table_name, record_id, session)
        return {"message": f"Record {record_id} deleted successfully from '{table_name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
