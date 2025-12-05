"""
Schema Builder Models - Store dynamic table definitions
Allows users to create custom tables, columns, and relationships
"""
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    pass  # Forward references will be handled by string annotations


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


class PublishStatus(str, Enum):
    """Publishing status for app components"""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    UNPUBLISHED = "UNPUBLISHED"


class FormFieldType(str, Enum):
    """Form field types"""
    TEXT = "text"
    EMAIL = "email"
    NUMBER = "number"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DATE = "date"
    DATETIME = "datetime"
    FILE = "file"


class WidgetType(str, Enum):
    """Dashboard widget types"""
    CHART = "chart"
    TABLE = "table"
    STAT = "stat"
    LIST = "list"
    CARD = "card"


class HTTPMethod(str, Enum):
    """HTTP methods for API endpoints"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


# ==================== App Model ====================
class AppBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(default="#3b82f6")
    is_active: bool = Field(default=True)


class App(AppBase, table=True):
    """Represents a complete application with multiple tables"""
    __tablename__ = "app"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    publish_status: PublishStatus = Field(default=PublishStatus.DRAFT)
    published_at: Optional[datetime] = None
    version: int = Field(default=1)
    
    # Relationships
    tables: List["TableSchema"] = Relationship(back_populates="app")
    pages: List["Page"] = Relationship(back_populates="app")
    forms: List["FormSchema"] = Relationship(back_populates="app")
    dashboards: List["DashboardConfig"] = Relationship(back_populates="app")
    api_endpoints: List["APIEndpoint"] = Relationship(back_populates="app")
    menus: List["MenuConfig"] = Relationship(back_populates="app")


class AppCreate(AppBase):
    pass


class AppUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None
    publish_status: Optional[PublishStatus] = None


class AppRead(AppBase):
    id: int
    created_at: datetime
    updated_at: datetime
    publish_status: PublishStatus
    published_at: Optional[datetime] = None
    version: int
    table_count: Optional[int] = None
    page_count: Optional[int] = None
    form_count: Optional[int] = None
    dashboard_count: Optional[int] = None
    api_count: Optional[int] = None
    menu_count: Optional[int] = None


# ==================== TableSchema Model ====================
class TableSchemaBase(SQLModel):
    name: str = Field(index=True)  # e.g., "customers", "orders"
    display_name: str  # e.g., "Customers", "Orders"
    description: Optional[str] = None
    icon: Optional[str] = None


class TableSchema(TableSchemaBase, table=True):
    """Stores metadata about dynamically created tables"""
    __tablename__ = "table_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="tables")
    columns: List["ColumnSchema"] = Relationship(
        back_populates="table",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    relationships_as_source: List["RelationshipSchema"] = Relationship(
        back_populates="source_table",
        sa_relationship_kwargs={"foreign_keys": "RelationshipSchema.source_table_id"}
    )
    relationships_as_target: List["RelationshipSchema"] = Relationship(
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


class ColumnSchema(ColumnSchemaBase, table=True):
    """Stores metadata about columns in dynamically created tables"""
    __tablename__ = "column_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    table_id: int = Field(foreign_key="table_schema.id")
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


# ==================== Page Model ====================
class PageBase(SQLModel):
    name: str = Field(index=True)
    title: str
    route: str  # URL route for the page
    description: Optional[str] = None
    icon: Optional[str] = None
    layout: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_active: bool = Field(default=True)


class Page(PageBase, table=True):
    """Pages within an application"""
    __tablename__ = "page"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="pages")


class PageCreate(PageBase):
    pass


class PageUpdate(SQLModel):
    title: Optional[str] = None
    route: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    layout: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PageRead(PageBase):
    id: int
    app_id: int
    created_at: datetime
    updated_at: datetime


# ==================== FormSchema Model ====================
class FormSchemaBase(SQLModel):
    name: str = Field(index=True)
    title: str
    description: Optional[str] = None
    table_name: Optional[str] = None  # Link to table for CRUD operations
    fields: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    validation_rules: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    layout: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    submit_action: Optional[str] = None
    is_active: bool = Field(default=True)


class FormSchema(FormSchemaBase, table=True):
    """Form configurations for data entry"""
    __tablename__ = "form_schema"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="forms")


class FormSchemaCreate(FormSchemaBase):
    pass


class FormSchemaUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    table_name: Optional[str] = None
    fields: Optional[List[Dict[str, Any]]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    layout: Optional[Dict[str, Any]] = None
    submit_action: Optional[str] = None
    is_active: Optional[bool] = None


class FormSchemaRead(FormSchemaBase):
    id: int
    app_id: int
    created_at: datetime
    updated_at: datetime


# ==================== DashboardConfig Model ====================
class DashboardConfigBase(SQLModel):
    name: str = Field(index=True)
    title: str
    description: Optional[str] = None
    widgets: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    layout: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    refresh_interval: Optional[int] = None  # seconds
    is_active: bool = Field(default=True)


class DashboardConfig(DashboardConfigBase, table=True):
    """Dashboard configurations with widgets"""
    __tablename__ = "dashboard_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="dashboards")


class DashboardConfigCreate(DashboardConfigBase):
    pass


class DashboardConfigUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    widgets: Optional[List[Dict[str, Any]]] = None
    layout: Optional[Dict[str, Any]] = None
    refresh_interval: Optional[int] = None
    is_active: Optional[bool] = None


class DashboardConfigRead(DashboardConfigBase):
    id: int
    app_id: int
    created_at: datetime
    updated_at: datetime


# ==================== APIEndpoint Model ====================
class APIEndpointBase(SQLModel):
    name: str = Field(index=True)
    path: str  # API path e.g., /api/v1/customers
    method: HTTPMethod
    description: Optional[str] = None
    table_name: Optional[str] = None  # Link to table for auto-generated CRUD
    request_schema: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    response_schema: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    authentication_required: bool = Field(default=False)
    custom_logic: Optional[str] = None  # Python code or SQL query
    is_active: bool = Field(default=True)


class APIEndpoint(APIEndpointBase, table=True):
    """Custom API endpoints for the application"""
    __tablename__ = "api_endpoint"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="api_endpoints")


class APIEndpointCreate(APIEndpointBase):
    pass


class APIEndpointUpdate(SQLModel):
    path: Optional[str] = None
    method: Optional[HTTPMethod] = None
    description: Optional[str] = None
    table_name: Optional[str] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    authentication_required: Optional[bool] = None
    custom_logic: Optional[str] = None
    is_active: Optional[bool] = None


class APIEndpointRead(APIEndpointBase):
    id: int
    app_id: int
    created_at: datetime
    updated_at: datetime


# ==================== MenuConfig Model ====================
class MenuConfigBase(SQLModel):
    name: str = Field(index=True)
    label: str
    icon: Optional[str] = None
    route: Optional[str] = None
    parent_id: Optional[int] = None
    order: int = Field(default=0)
    is_active: bool = Field(default=True)
    permissions: List[str] = Field(default=[], sa_column=Column(JSON))


class MenuConfig(MenuConfigBase, table=True):
    """Navigation menu configuration"""
    __tablename__ = "menu_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    app: Optional[App] = Relationship(back_populates="menus")


class MenuConfigCreate(MenuConfigBase):
    pass


class MenuConfigUpdate(SQLModel):
    label: Optional[str] = None
    icon: Optional[str] = None
    route: Optional[str] = None
    parent_id: Optional[int] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None
    permissions: Optional[List[str]] = None


class MenuConfigRead(MenuConfigBase):
    id: int
    app_id: int
    created_at: datetime
    updated_at: datetime


# ==================== Read Models (defined after all base models) ====================
class TableSchemaRead(TableSchemaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    columns: List[ColumnSchemaRead] = []
    record_count: Optional[int] = None
