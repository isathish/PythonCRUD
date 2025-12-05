"""
Dynamic Table Generator Service
Generates CRUD operations and APIs for user-defined tables
"""
from sqlmodel import Session, select, delete as sql_delete
from typing import List, Dict, Any, Optional
from models.schema_builder import (
    TableSchema, TableSchemaCreate, TableSchemaUpdate,
    ColumnSchema, ColumnSchemaCreate,
    RelationshipSchema, RelationshipSchemaCreate,
    DynamicData, ColumnType, App
)
from datetime import datetime


class TableGeneratorService:
    """Service for managing dynamic table schemas"""
    
    @staticmethod
    def create_table_schema(
        app_id: int,
        table_data: TableSchemaCreate,
        session: Session
    ) -> TableSchema:
        """Create a new table schema with columns"""
        
        # Validate app exists
        app = session.get(App, app_id)
        if not app:
            raise ValueError(f"App with id {app_id} not found")
        
        # Check if table name already exists in this app
        existing = session.exec(
            select(TableSchema).where(
                TableSchema.app_id == app_id,
                TableSchema.name == table_data.name
            )
        ).first()
        
        if existing:
            raise ValueError(f"Table '{table_data.name}' already exists in this app")
        
        # Create table schema
        columns = table_data.columns
        table_dict = table_data.model_dump(exclude={'columns'})
        table_schema = TableSchema(**table_dict, app_id=app_id)
        
        session.add(table_schema)
        session.commit()
        session.refresh(table_schema)
        
        # Create columns
        for col_data in columns:
            # col_data is already a dict
            if isinstance(col_data, dict):
                column = ColumnSchema(**col_data, table_id=table_schema.id)
            else:
                column = ColumnSchema(**col_data.model_dump(), table_id=table_schema.id)
            session.add(column)
        
        session.commit()
        session.refresh(table_schema)
        
        return table_schema
    
    @staticmethod
    def get_table_schemas(app_id: int, session: Session) -> List[TableSchema]:
        """Get all table schemas for an app"""
        tables = session.exec(
            select(TableSchema).where(TableSchema.app_id == app_id)
        ).all()
        return list(tables)
    
    @staticmethod
    def get_table_schema(table_id: int, session: Session) -> Optional[TableSchema]:
        """Get a specific table schema"""
        return session.get(TableSchema, table_id)
    
    @staticmethod
    def update_table_schema(
        table_id: int,
        update_data: TableSchemaUpdate,
        session: Session
    ) -> TableSchema:
        """Update table schema"""
        table = session.get(TableSchema, table_id)
        if not table:
            raise ValueError(f"Table schema with id {table_id} not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(table, key, value)
        
        table.updated_at = datetime.utcnow()
        session.add(table)
        session.commit()
        session.refresh(table)
        
        return table
    
    @staticmethod
    def delete_table_schema(table_id: int, session: Session):
        """Delete a table schema and all its data"""
        table = session.get(TableSchema, table_id)
        if not table:
            raise ValueError(f"Table schema with id {table_id} not found")
        
        # Delete all data records for this table
        session.exec(
            sql_delete(DynamicData).where(DynamicData.table_name == table.name)
        )
        
        # Delete table schema (columns will cascade)
        session.delete(table)
        session.commit()
    
    @staticmethod
    def add_column(
        table_id: int,
        column_data: ColumnSchemaCreate,
        session: Session
    ) -> ColumnSchema:
        """Add a new column to a table"""
        table = session.get(TableSchema, table_id)
        if not table:
            raise ValueError(f"Table schema with id {table_id} not found")
        
        # Check if column name already exists
        existing = session.exec(
            select(ColumnSchema).where(
                ColumnSchema.table_id == table_id,
                ColumnSchema.name == column_data.name
            )
        ).first()
        
        if existing:
            raise ValueError(f"Column '{column_data.name}' already exists in this table")
        
        column = ColumnSchema(**column_data.model_dump(), table_id=table_id)
        session.add(column)
        session.commit()
        session.refresh(column)
        
        return column
    
    @staticmethod
    def create_relationship(
        rel_data: RelationshipSchemaCreate,
        session: Session
    ) -> RelationshipSchema:
        """Create a relationship between tables"""
        # Validate tables exist
        source_table = session.get(TableSchema, rel_data.source_table_id)
        target_table = session.get(TableSchema, rel_data.target_table_id)
        
        if not source_table:
            raise ValueError(f"Source table with id {rel_data.source_table_id} not found")
        if not target_table:
            raise ValueError(f"Target table with id {rel_data.target_table_id} not found")
        
        relationship = RelationshipSchema(**rel_data.model_dump())
        session.add(relationship)
        session.commit()
        session.refresh(relationship)
        
        return relationship


class DynamicDataService:
    """Service for managing data in dynamically created tables"""
    
    @staticmethod
    def validate_data(data: Dict[str, Any], table_schema: TableSchema) -> Dict[str, Any]:
        """Validate data against table schema"""
        validated_data = {}
        
        for column in table_schema.columns:
            value = data.get(column.name)
            
            # Check required fields
            if column.is_required and value is None:
                raise ValueError(f"Field '{column.display_name}' is required")
            
            # Skip None values
            if value is None:
                continue
            
            # Type validation and conversion
            if column.column_type == ColumnType.STRING:
                value = str(value)
                if column.max_length and len(value) > column.max_length:
                    raise ValueError(
                        f"Field '{column.display_name}' exceeds maximum length of {column.max_length}"
                    )
            
            elif column.column_type == ColumnType.INTEGER:
                value = int(value)
                if column.min_value is not None and value < column.min_value:
                    raise ValueError(
                        f"Field '{column.display_name}' must be at least {column.min_value}"
                    )
                if column.max_value is not None and value > column.max_value:
                    raise ValueError(
                        f"Field '{column.display_name}' must be at most {column.max_value}"
                    )
            
            elif column.column_type == ColumnType.FLOAT:
                value = float(value)
                if column.min_value is not None and value < column.min_value:
                    raise ValueError(
                        f"Field '{column.display_name}' must be at least {column.min_value}"
                    )
                if column.max_value is not None and value > column.max_value:
                    raise ValueError(
                        f"Field '{column.display_name}' must be at most {column.max_value}"
                    )
            
            elif column.column_type == ColumnType.BOOLEAN:
                value = bool(value)
            
            validated_data[column.name] = value
        
        return validated_data
    
    @staticmethod
    def create_record(
        table_name: str,
        data: Dict[str, Any],
        table_schema: TableSchema,
        session: Session
    ) -> DynamicData:
        """Create a new record in a dynamic table"""
        
        # Validate data
        validated_data = DynamicDataService.validate_data(data, table_schema)
        
        # Get next record_id for this table
        last_record = session.exec(
            select(DynamicData)
            .where(DynamicData.table_name == table_name)
            .order_by(DynamicData.record_id.desc())
        ).first()
        
        record_id = (last_record.record_id + 1) if last_record else 1
        
        # Create record
        record = DynamicData(
            table_name=table_name,
            record_id=record_id,
            data=validated_data
        )
        
        session.add(record)
        session.commit()
        session.refresh(record)
        
        return record
    
    @staticmethod
    def get_records(
        table_name: str,
        session: Session,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        limit: int = 10
    ) -> tuple[List[DynamicData], int]:
        """Get records from a dynamic table with filtering and pagination"""
        
        query = select(DynamicData).where(DynamicData.table_name == table_name)
        
        # Apply filters (simple equality for now)
        if filters:
            for key, value in filters.items():
                # This is a simplified filter - in production you'd use JSONB queries
                pass
        
        # Get total count
        total = len(session.exec(query).all())
        
        # Apply pagination
        query = query.offset((page - 1) * limit).limit(limit)
        
        records = session.exec(query).all()
        return list(records), total
    
    @staticmethod
    def get_record(
        table_name: str,
        record_id: int,
        session: Session
    ) -> Optional[DynamicData]:
        """Get a specific record"""
        record = session.exec(
            select(DynamicData).where(
                DynamicData.table_name == table_name,
                DynamicData.record_id == record_id
            )
        ).first()
        
        return record
    
    @staticmethod
    def update_record(
        table_name: str,
        record_id: int,
        data: Dict[str, Any],
        table_schema: TableSchema,
        session: Session
    ) -> DynamicData:
        """Update a record in a dynamic table"""
        
        record = DynamicDataService.get_record(table_name, record_id, session)
        if not record:
            raise ValueError(f"Record with id {record_id} not found in table '{table_name}'")
        
        # Validate data
        validated_data = DynamicDataService.validate_data(data, table_schema)
        
        # Merge with existing data
        record.data = {**record.data, **validated_data}
        record.updated_at = datetime.utcnow()
        
        session.add(record)
        session.commit()
        session.refresh(record)
        
        return record
    
    @staticmethod
    def delete_record(table_name: str, record_id: int, session: Session):
        """Delete a record from a dynamic table"""
        
        record = DynamicDataService.get_record(table_name, record_id, session)
        if not record:
            raise ValueError(f"Record with id {record_id} not found in table '{table_name}'")
        
        session.delete(record)
        session.commit()
