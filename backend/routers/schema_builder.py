"""
Schema Builder Router - Manage table schemas
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from core.database import get_session
from models.schema_builder import (
    TableSchema, TableSchemaCreate, TableSchemaUpdate, TableSchemaRead,
    ColumnSchema, ColumnSchemaCreate, ColumnSchemaRead,
    RelationshipSchema, RelationshipSchemaCreate, RelationshipSchemaRead,
    DynamicData
)
from services.table_generator_service import TableGeneratorService
from sqlmodel import select

router = APIRouter(prefix="/schema", tags=["schema-builder"])


# ==================== Table Schema Endpoints ====================
@router.post("/apps/{app_id}/tables", response_model=TableSchemaRead)
def create_table_schema(
    app_id: int,
    table: TableSchemaCreate,
    session: Session = Depends(get_session)
):
    """Create a new table schema with columns"""
    try:
        db_table = TableGeneratorService.create_table_schema(app_id, table, session)
        return TableSchemaRead(
            **db_table.model_dump(),
            columns=[ColumnSchemaRead(**col.model_dump()) for col in db_table.columns],
            record_count=0
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/apps/{app_id}/tables", response_model=List[TableSchemaRead])
def list_table_schemas(app_id: int, session: Session = Depends(get_session)):
    """List all table schemas for an app"""
    tables = TableGeneratorService.get_table_schemas(app_id, session)
    
    result = []
    for table in tables:
        # Count records
        record_count = len(
            session.exec(
                select(DynamicData).where(DynamicData.table_name == table.name)
            ).all()
        )
        
        result.append(TableSchemaRead(
            **table.model_dump(),
            columns=[ColumnSchemaRead(**col.model_dump()) for col in table.columns],
            record_count=record_count
        ))
    
    return result


@router.get("/tables/{table_id}", response_model=TableSchemaRead)
def get_table_schema(table_id: int, session: Session = Depends(get_session)):
    """Get a specific table schema"""
    table = TableGeneratorService.get_table_schema(table_id, session)
    if not table:
        raise HTTPException(status_code=404, detail=f"Table schema with id {table_id} not found")
    
    # Count records
    record_count = len(
        session.exec(
            select(DynamicData).where(DynamicData.table_name == table.name)
        ).all()
    )
    
    return TableSchemaRead(
        **table.model_dump(),
        columns=[ColumnSchemaRead(**col.model_dump()) for col in table.columns],
        record_count=record_count
    )


@router.put("/tables/{table_id}", response_model=TableSchemaRead)
def update_table_schema(
    table_id: int,
    table_update: TableSchemaUpdate,
    session: Session = Depends(get_session)
):
    """Update a table schema"""
    try:
        table = TableGeneratorService.update_table_schema(table_id, table_update, session)
        
        # Count records
        record_count = len(
            session.exec(
                select(DynamicData).where(DynamicData.table_name == table.name)
            ).all()
        )
        
        return TableSchemaRead(
            **table.model_dump(),
            columns=[ColumnSchemaRead(**col.model_dump()) for col in table.columns],
            record_count=record_count
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/tables/{table_id}")
def delete_table_schema(table_id: int, session: Session = Depends(get_session)):
    """Delete a table schema and all its data"""
    try:
        TableGeneratorService.delete_table_schema(table_id, session)
        return {"message": "Table schema deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Column Endpoints ====================
@router.post("/tables/{table_id}/columns", response_model=ColumnSchemaRead)
def add_column(
    table_id: int,
    column: ColumnSchemaCreate,
    session: Session = Depends(get_session)
):
    """Add a new column to a table"""
    try:
        db_column = TableGeneratorService.add_column(table_id, column, session)
        return ColumnSchemaRead(**db_column.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Relationship Endpoints ====================
@router.post("/relationships", response_model=RelationshipSchemaRead)
def create_relationship(
    relationship: RelationshipSchemaCreate,
    session: Session = Depends(get_session)
):
    """Create a relationship between tables"""
    try:
        db_rel = TableGeneratorService.create_relationship(relationship, session)
        return RelationshipSchemaRead(**db_rel.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/apps/{app_id}/relationships", response_model=List[RelationshipSchemaRead])
def list_relationships(app_id: int, session: Session = Depends(get_session)):
    """List all relationships for tables in an app"""
    # Get all tables in the app
    tables = TableGeneratorService.get_table_schemas(app_id, session)
    table_ids = [t.id for t in tables]
    
    # Get all relationships involving these tables
    relationships = session.exec(
        select(RelationshipSchema).where(
            (RelationshipSchema.source_table_id.in_(table_ids)) |
            (RelationshipSchema.target_table_id.in_(table_ids))
        )
    ).all()
    
    return [RelationshipSchemaRead(**rel.model_dump()) for rel in relationships]
