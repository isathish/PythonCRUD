"""
Schema Builder Models - Store dynamic table definitions
Allows users to create custom tables, columns, and relationships
"""
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime
from enum import Enum


class ColumnType(str, Enum):
    """Supported column data types"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TEXT = "text"
    JSON = "json"


class RelationType(str, Enum):
    """Types of relationships"""
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"


# ==================== App Model ====================
class AppBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(default="#3b82f6")
    is_active: bool = Field(default=True)


class App(AppBase, table=True):
    """Represents a complete application with multiple tables"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tables = Relationship(back_populates="app")


class AppCreate(AppBase):
    pass


class AppUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class AppRead(AppBase):
    id: int
    created_at: datetime
    updated_at: datetime
    table_count: Optional[int] = None


# ==================== TableSchema Model ====================
class TableSchemaBase(SQLModel):
    name: str = Field(index=True)  # e.g., "customers", "orders"
    display_name: str  # e.g., "Customers", "Orders"
    description: Optional[str] = None
    icon: Optional[str] = None
    app_id: int = Field(foreign_key="app.id")


class TableSchema(TableSchemaBase, table=True):
    """Stores metadata about dynamically created tables"""
    __tablename__ = "table_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="tables")
    columns = Relationship(
        back_populates="table",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    relationships_as_source = Relationship(
        back_populates="source_table",
        sa_relationship_kwargs={"foreign_keys": "RelationshipSchema.source_table_id"}
    )
    relationships_as_target = Relationship(
        back_populates="target_table",
        sa_relationship_kwargs={"foreign_keys": "RelationshipSchema.target_table_id"}
    )


class TableSchemaCreate(TableSchemaBase):
    columns: List[Dict[str, Any]] = []


class TableSchemaUpdate(SQLModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# ==================== ColumnSchema Model ====================
class ColumnSchemaBase(SQLModel):
    name: str  # e.g., "email", "phone_number"
    display_name: str  # e.g., "Email Address", "Phone Number"
    column_type: ColumnType
    is_required: bool = Field(default=False)
    is_unique: bool = Field(default=False)
    default_value: Optional[str] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    validation_regex: Optional[str] = None
    help_text: Optional[str] = None
    table_id: int = Field(foreign_key="table_schema.id")


class ColumnSchema(ColumnSchemaBase, table=True):
    """Stores metadata about columns in dynamically created tables"""
    __tablename__ = "column_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    table: Optional[TableSchema] = Relationship(back_populates="columns")


class ColumnSchemaCreate(SQLModel):
    name: str
    display_name: str
    column_type: ColumnType
    is_required: bool = False
    is_unique: bool = False
    default_value: Optional[str] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    validation_regex: Optional[str] = None
    help_text: Optional[str] = None


class ColumnSchemaUpdate(SQLModel):
    display_name: Optional[str] = None
    is_required: Optional[bool] = None
    default_value: Optional[str] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    validation_regex: Optional[str] = None
    help_text: Optional[str] = None


class ColumnSchemaRead(ColumnSchemaBase):
    id: int
    created_at: datetime


# ==================== RelationshipSchema Model ====================
class RelationshipSchemaBase(SQLModel):
    name: str  # e.g., "customer_orders"
    relation_type: RelationType
    source_table_id: int = Field(foreign_key="table_schema.id")
    target_table_id: int = Field(foreign_key="table_schema.id")
    source_column: Optional[str] = None  # Foreign key column name
    target_column: Optional[str] = None  # Referenced column name


class RelationshipSchema(RelationshipSchemaBase, table=True):
    """Stores relationships between dynamically created tables"""
    __tablename__ = "relationship_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    source_table: Optional[TableSchema] = Relationship(
        back_populates="relationships_as_source",
        sa_relationship_kwargs={"foreign_keys": "[RelationshipSchema.source_table_id]"}
    )
    target_table: Optional[TableSchema] = Relationship(
        back_populates="relationships_as_target",
        sa_relationship_kwargs={"foreign_keys": "[RelationshipSchema.target_table_id]"}
    )


class RelationshipSchemaCreate(RelationshipSchemaBase):
    pass


class RelationshipSchemaRead(RelationshipSchemaBase):
    id: int
    created_at: datetime


# ==================== DynamicData Model ====================
class DynamicDataBase(SQLModel):
    """Stores actual data for dynamically created tables"""
    table_name: str = Field(index=True)
    record_id: int
    data: Dict[str, Any] = Field(sa_column=Column(JSON))


class DynamicData(DynamicDataBase, table=True):
    """Generic storage for dynamic table records"""
    __tablename__ = "dynamic_data"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DynamicDataCreate(SQLModel):
    data: Dict[str, Any]


class DynamicDataUpdate(SQLModel):
    data: Dict[str, Any]


class DynamicDataRead(DynamicDataBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==================== Read Models (defined after all base models) ====================
class TableSchemaRead(TableSchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    columns: List[ColumnSchemaRead] = []
    record_count: Optional[int] = None
