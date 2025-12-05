"""
Seed script for Meta-CRUD Builder System
Creates sample applications with tables, columns, and data
"""
import asyncio
from sqlmodel import Session, select
from core.database import engine, create_db_and_tables
from models.schema_builder import (
    App, TableSchema, ColumnSchema, DynamicData, ColumnType
)
from services.table_generator_service import TableGeneratorService, DynamicDataService
from datetime import datetime


def seed_apps():
    """Create sample apps with tables and data"""
    
    create_db_and_tables()
    
    with Session(engine) as session:
        # Clear existing data
        print("Clearing existing meta-CRUD data...")
        session.exec(select(DynamicData)).all()
        for record in session.exec(select(DynamicData)):
            session.delete(record)
        for col in session.exec(select(ColumnSchema)):
            session.delete(col)
        for table in session.exec(select(TableSchema)):
            session.delete(table)
        for app in session.exec(select(App)):
            session.delete(app)
        session.commit()
        
        print("\n" + "="*60)
        print("SEEDING META-CRUD BUILDER SYSTEM")
        print("="*60 + "\n")
        
        # ==================== App 1: CRM System ====================
        print("📦 Creating App: CRM System")
        crm_app = App(
            name="crm_system",
            display_name="CRM System",
            description="Customer Relationship Management",
            icon="💼",
            color="#3B82F6",
            is_active=True
        )
        session.add(crm_app)
        session.commit()
        session.refresh(crm_app)
        print(f"   ✓ App created (ID: {crm_app.id})")
        
        # Table: Customers
        print("   📊 Creating table: Customers")
        customers_table = TableSchema(
            name="customers",
            display_name="Customers",
            description="Customer contact information",
            app_id=crm_app.id
        )
        session.add(customers_table)
        session.commit()
        session.refresh(customers_table)
        
        # Columns for Customers
        customer_columns = [
            ColumnSchema(
                table_id=customers_table.id,
                name="name",
                display_name="Full Name",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=100,
                help_text="Customer's full name"
            ),
            ColumnSchema(
                table_id=customers_table.id,
                name="email",
                display_name="Email Address",
                column_type=ColumnType.STRING,
                is_required=True,
                is_unique=True,
                max_length=255,
                help_text="Primary email address"
            ),
            ColumnSchema(
                table_id=customers_table.id,
                name="phone",
                display_name="Phone Number",
                column_type=ColumnType.STRING,
                max_length=20,
                help_text="Contact phone number"
            ),
            ColumnSchema(
                table_id=customers_table.id,
                name="company",
                display_name="Company",
                column_type=ColumnType.STRING,
                max_length=100
            ),
            ColumnSchema(
                table_id=customers_table.id,
                name="status",
                display_name="Status",
                column_type=ColumnType.STRING,
                is_required=True,
                default_value="active",
                help_text="Customer status: active, inactive, lead"
            )
        ]
        for col in customer_columns:
            session.add(col)
        session.commit()
        print(f"      ✓ Added {len(customer_columns)} columns")
        
        # Sample customer data
        customer_data = [
            {"name": "John Smith", "email": "john@example.com", "phone": "+1-555-0101", "company": "Tech Corp", "status": "active"},
            {"name": "Sarah Johnson", "email": "sarah@example.com", "phone": "+1-555-0102", "company": "Design Studio", "status": "active"},
            {"name": "Mike Chen", "email": "mike@example.com", "phone": "+1-555-0103", "company": "StartupXYZ", "status": "lead"},
            {"name": "Emily Brown", "email": "emily@example.com", "phone": "+1-555-0104", "company": "Consulting Inc", "status": "active"},
            {"name": "David Wilson", "email": "david@example.com", "phone": "+1-555-0105", "company": "Marketing Pro", "status": "inactive"}
        ]
        
        for i, data in enumerate(customer_data, 1):
            record = DynamicData(
                table_name="customers",
                record_id=i,
                data=data
            )
            session.add(record)
        session.commit()
        print(f"      ✓ Added {len(customer_data)} customer records\n")
        
        
        # ==================== App 2: E-Commerce ====================
        print("📦 Creating App: E-Commerce")
        ecommerce_app = App(
            name="ecommerce",
            display_name="E-Commerce",
            description="Online store management",
            icon="🛒",
            color="#10B981",
            is_active=True
        )
        session.add(ecommerce_app)
        session.commit()
        session.refresh(ecommerce_app)
        print(f"   ✓ App created (ID: {ecommerce_app.id})")
        
        # Table: Products
        print("   📊 Creating table: Products")
        products_table = TableSchema(
            name="products",
            display_name="Products",
            description="Product catalog",
            app_id=ecommerce_app.id
        )
        session.add(products_table)
        session.commit()
        session.refresh(products_table)
        
        product_columns = [
            ColumnSchema(
                table_id=products_table.id,
                name="name",
                display_name="Product Name",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=200
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="sku",
                display_name="SKU",
                column_type=ColumnType.STRING,
                is_required=True,
                is_unique=True,
                max_length=50,
                help_text="Stock Keeping Unit"
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="price",
                display_name="Price",
                column_type=ColumnType.FLOAT,
                is_required=True,
                min_value=0.0,
                help_text="Product price in USD"
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="stock",
                display_name="Stock Quantity",
                column_type=ColumnType.INTEGER,
                is_required=True,
                min_value=0,
                default_value="0"
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="category",
                display_name="Category",
                column_type=ColumnType.STRING,
                max_length=50
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="in_stock",
                display_name="In Stock",
                column_type=ColumnType.BOOLEAN,
                is_required=True,
                default_value="true"
            ),
            ColumnSchema(
                table_id=products_table.id,
                name="description",
                display_name="Description",
                column_type=ColumnType.TEXT,
                help_text="Detailed product description"
            )
        ]
        for col in product_columns:
            session.add(col)
        session.commit()
        print(f"      ✓ Added {len(product_columns)} columns")
        
        product_data = [
            {"name": "Wireless Mouse", "sku": "WM-001", "price": 29.99, "stock": 150, "category": "Electronics", "in_stock": True, "description": "Ergonomic wireless mouse with USB receiver"},
            {"name": "Mechanical Keyboard", "sku": "KB-002", "price": 89.99, "stock": 75, "category": "Electronics", "in_stock": True, "description": "RGB mechanical gaming keyboard"},
            {"name": "USB-C Cable", "sku": "CB-003", "price": 12.99, "stock": 300, "category": "Accessories", "in_stock": True, "description": "6ft USB-C charging cable"},
            {"name": "Laptop Stand", "sku": "LS-004", "price": 45.00, "stock": 0, "category": "Accessories", "in_stock": False, "description": "Adjustable aluminum laptop stand"},
            {"name": "Webcam HD", "sku": "WC-005", "price": 65.00, "stock": 45, "category": "Electronics", "in_stock": True, "description": "1080p HD webcam with microphone"},
            {"name": "Desk Mat", "sku": "DM-006", "price": 24.99, "stock": 120, "category": "Accessories", "in_stock": True, "description": "Large desk mat 36x18 inches"}
        ]
        
        for i, data in enumerate(product_data, 1):
            record = DynamicData(
                table_name="products",
                record_id=i,
                data=data
            )
            session.add(record)
        session.commit()
        print(f"      ✓ Added {len(product_data)} product records\n")
        
        
        # ==================== App 3: HR Management ====================
        print("📦 Creating App: HR Management")
        hr_app = App(
            name="hr_management",
            display_name="HR Management",
            description="Human Resources and employee tracking",
            icon="👥",
            color="#F59E0B",
            is_active=True
        )
        session.add(hr_app)
        session.commit()
        session.refresh(hr_app)
        print(f"   ✓ App created (ID: {hr_app.id})")
        
        # Table: Employees
        print("   📊 Creating table: Employees")
        employees_table = TableSchema(
            name="employees",
            display_name="Employees",
            description="Employee records",
            app_id=hr_app.id
        )
        session.add(employees_table)
        session.commit()
        session.refresh(employees_table)
        
        employee_columns = [
            ColumnSchema(
                table_id=employees_table.id,
                name="employee_id",
                display_name="Employee ID",
                column_type=ColumnType.STRING,
                is_required=True,
                is_unique=True,
                max_length=20
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="full_name",
                display_name="Full Name",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=100
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="email",
                display_name="Work Email",
                column_type=ColumnType.STRING,
                is_required=True,
                is_unique=True,
                max_length=255
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="department",
                display_name="Department",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=50
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="position",
                display_name="Position",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=100
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="hire_date",
                display_name="Hire Date",
                column_type=ColumnType.DATE,
                is_required=True
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="salary",
                display_name="Annual Salary",
                column_type=ColumnType.FLOAT,
                min_value=0.0
            ),
            ColumnSchema(
                table_id=employees_table.id,
                name="is_active",
                display_name="Active Employee",
                column_type=ColumnType.BOOLEAN,
                is_required=True,
                default_value="true"
            )
        ]
        for col in employee_columns:
            session.add(col)
        session.commit()
        print(f"      ✓ Added {len(employee_columns)} columns")
        
        employee_data = [
            {"employee_id": "EMP001", "full_name": "Alice Cooper", "email": "alice@company.com", "department": "Engineering", "position": "Senior Developer", "hire_date": "2020-03-15", "salary": 95000.0, "is_active": True},
            {"employee_id": "EMP002", "full_name": "Bob Martinez", "email": "bob@company.com", "department": "Engineering", "position": "DevOps Engineer", "hire_date": "2021-06-01", "salary": 88000.0, "is_active": True},
            {"employee_id": "EMP003", "full_name": "Carol White", "email": "carol@company.com", "department": "Marketing", "position": "Marketing Manager", "hire_date": "2019-01-10", "salary": 85000.0, "is_active": True},
            {"employee_id": "EMP004", "full_name": "Dan Lee", "email": "dan@company.com", "department": "Sales", "position": "Sales Representative", "hire_date": "2022-09-15", "salary": 65000.0, "is_active": True},
            {"employee_id": "EMP005", "full_name": "Eve Taylor", "email": "eve@company.com", "department": "HR", "position": "HR Specialist", "hire_date": "2021-11-01", "salary": 72000.0, "is_active": True},
            {"employee_id": "EMP006", "full_name": "Frank Green", "email": "frank@company.com", "department": "Engineering", "position": "Junior Developer", "hire_date": "2023-02-20", "salary": 68000.0, "is_active": False}
        ]
        
        for i, data in enumerate(employee_data, 1):
            record = DynamicData(
                table_name="employees",
                record_id=i,
                data=data
            )
            session.add(record)
        session.commit()
        print(f"      ✓ Added {len(employee_data)} employee records\n")
        
        
        # ==================== App 4: Task Manager ====================
        print("📦 Creating App: Task Manager")
        tasks_app = App(
            name="task_manager",
            display_name="Task Manager",
            description="Project and task tracking",
            icon="📋",
            color="#8B5CF6",
            is_active=True
        )
        session.add(tasks_app)
        session.commit()
        session.refresh(tasks_app)
        print(f"   ✓ App created (ID: {tasks_app.id})")
        
        # Table: Tasks
        print("   📊 Creating table: Tasks")
        tasks_table = TableSchema(
            name="tasks",
            display_name="Tasks",
            description="Task tracking and management",
            app_id=tasks_app.id
        )
        session.add(tasks_table)
        session.commit()
        session.refresh(tasks_table)
        
        task_columns = [
            ColumnSchema(
                table_id=tasks_table.id,
                name="title",
                display_name="Task Title",
                column_type=ColumnType.STRING,
                is_required=True,
                max_length=200
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="description",
                display_name="Description",
                column_type=ColumnType.TEXT
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="status",
                display_name="Status",
                column_type=ColumnType.STRING,
                is_required=True,
                default_value="todo",
                help_text="Status: todo, in_progress, review, done"
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="priority",
                display_name="Priority",
                column_type=ColumnType.INTEGER,
                is_required=True,
                min_value=1,
                max_value=5,
                default_value="3",
                help_text="1=Low, 5=Critical"
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="assignee",
                display_name="Assigned To",
                column_type=ColumnType.STRING,
                max_length=100
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="due_date",
                display_name="Due Date",
                column_type=ColumnType.DATE
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="estimated_hours",
                display_name="Estimated Hours",
                column_type=ColumnType.FLOAT,
                min_value=0.0
            ),
            ColumnSchema(
                table_id=tasks_table.id,
                name="metadata",
                display_name="Metadata",
                column_type=ColumnType.JSON,
                help_text="Additional task metadata"
            )
        ]
        for col in task_columns:
            session.add(col)
        session.commit()
        print(f"      ✓ Added {len(task_columns)} columns")
        
        task_data = [
            {"title": "Design new landing page", "description": "Create mockups for the new homepage", "status": "in_progress", "priority": 4, "assignee": "Carol White", "due_date": "2025-12-10", "estimated_hours": 16.0, "metadata": {"tags": ["design", "ui"]}},
            {"title": "Fix login bug", "description": "Users can't login with special characters in password", "status": "todo", "priority": 5, "assignee": "Alice Cooper", "due_date": "2025-12-08", "estimated_hours": 4.0, "metadata": {"tags": ["bug", "urgent"]}},
            {"title": "Update documentation", "description": "Add API documentation for new endpoints", "status": "review", "priority": 2, "assignee": "Bob Martinez", "due_date": "2025-12-15", "estimated_hours": 8.0, "metadata": {"tags": ["docs"]}},
            {"title": "Database migration", "description": "Migrate production database to new server", "status": "todo", "priority": 5, "assignee": "Bob Martinez", "due_date": "2025-12-12", "estimated_hours": 12.0, "metadata": {"tags": ["infrastructure", "critical"]}},
            {"title": "Setup CI/CD pipeline", "description": "Configure automated testing and deployment", "status": "done", "priority": 3, "assignee": "Bob Martinez", "due_date": "2025-12-01", "estimated_hours": 20.0, "metadata": {"tags": ["devops"]}},
            {"title": "Customer onboarding flow", "description": "Improve new customer onboarding experience", "status": "in_progress", "priority": 3, "assignee": "Dan Lee", "due_date": "2025-12-20", "estimated_hours": 24.0, "metadata": {"tags": ["ux", "sales"]}},
            {"title": "Security audit", "description": "Conduct security review of authentication system", "status": "todo", "priority": 4, "assignee": "Alice Cooper", "due_date": "2025-12-18", "estimated_hours": 16.0, "metadata": {"tags": ["security"]}}
        ]
        
        for i, data in enumerate(task_data, 1):
            record = DynamicData(
                table_name="tasks",
                record_id=i,
                data=data
            )
            session.add(record)
        session.commit()
        print(f"      ✓ Added {len(task_data)} task records\n")
        
        
        print("="*60)
        print("✅ SEEDING COMPLETE!")
        print("="*60)
        print(f"\nCreated:")
        print(f"  • 4 Applications")
        print(f"  • 4 Tables")
        print(f"  • {len(customer_columns) + len(product_columns) + len(employee_columns) + len(task_columns)} Columns")
        print(f"  • {len(customer_data) + len(product_data) + len(employee_data) + len(task_data)} Data Records")
        print(f"\nAccess the system at: http://localhost:3000")
        print(f"Go to 'App Builder' to see all the sample apps!\n")


if __name__ == "__main__":
    seed_apps()
