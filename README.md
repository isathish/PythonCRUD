# Dynamic CRUD Builder System

A complete **meta-CRUD system** that allows users to visually create database tables, define schemas, and automatically generate CRUD interfaces and APIs. This is a production-grade application with Docker Compose orchestration, PostgreSQL database, and a modern React frontend.

## 🎯 What This System Does

This is not just a CRUD application - it's a **CRUD generator**! Users can:

1. **Create Custom Applications** - Group related tables into applications
2. **Design Tables Visually** - Define columns, data types, validations, and constraints
3. **Auto-Generate CRUD APIs** - Get REST endpoints automatically for your tables
4. **Manage Data** - Full CRUD interface with smart form rendering based on column types
5. **Advanced Filtering** - 11 filter operators with AND/OR logic
6. **Dashboard Builder** - Create custom dashboards with metrics, charts, and tables

## 🏗️ Architecture

### Backend (FastAPI + PostgreSQL)
- **Framework**: FastAPI 0.109 with automatic OpenAPI docs
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: PostgreSQL 15
- **Features**:
  - Dynamic table schema management
  - Generic JSON storage for flexible data
  - Validation engine (required, unique, max_length, min/max values, regex)
  - Advanced query filtering (11 operators)
  - Dashboard engine (metrics, bar/pie/line/donut charts)

### Frontend (React + Vite)
- **Framework**: React 18 with Vite 5
- **Styling**: Tailwind CSS 3
- **Charts**: Recharts 2
- **Features**:
  - App Builder - Create and manage applications
  - Table Designer - Visual table creator with column management
  - Dynamic Data Manager - Auto-generated CRUD forms
  - Advanced Filter Builder - Visual query builder
  - Responsive design with modern UI

### Infrastructure
- **Docker Compose** - 3 services (db, backend, frontend)
- **PostgreSQL** - Data persistence with JSON column support
- **Hot Reload** - Enabled for both frontend and backend

## 🚀 Getting Started

### Prerequisites
- Docker Desktop installed and running
- Ports 3000, 8000, 5432 available

### Quick Start

1. **Start all containers**:
```bash
cd PythonCRUD
docker-compose up -d
```

2. **Wait for healthy status** (check with `docker-compose ps`)

3. **Access the application**:
   - **Frontend**: http://localhost:3000
   - **Backend API Docs**: http://localhost:8000/docs
   - **PostgreSQL**: localhost:5432

4. **Seed sample data** (optional):
```bash
docker-compose exec backend python seed_data.py
```

## 💡 How to Use

### 1. Create an Application

Navigate to **App Builder** (🔧 icon in sidebar):
1. Click "Create New App"
2. Fill in details:
   - **App Name**: `my_crm` (lowercase, no spaces)
   - **Display Name**: `My CRM`
   - **Description**: `Customer relationship management`
   - **Icon**: Choose from emoji library
   - **Color**: Pick theme color
3. Click "Create App"

### 2. Design a Table

Click "Manage Tables" on your app:
1. Click "Create Table"
2. Define table:
   - **Table Name**: `customers`
   - **Display Name**: `Customers`
3. Click "Add Column" to add fields:
   - **Name**: `email`
   - **Display Name**: `Email Address`
   - **Type**: `string`
   - **Required**: ✅
   - **Unique**: ✅
   - **Max Length**: `255`
   - **Help Text**: `Customer's email address`

**Column Types Available**:
- `string` - Short text (with max_length)
- `text` - Long text (unlimited)
- `integer` - Whole numbers (with min/max)
- `float` - Decimal numbers (with min/max)
- `boolean` - True/False
- `date` - Date only
- `datetime` - Date + Time
- `json` - Structured data

**Validations Available**:
- Required (not null)
- Unique (no duplicates)
- Max Length (for strings)
- Min/Max Value (for numbers)
- Regex Pattern (custom validation)
- Default Value

### 3. Manage Data

Click "Manage Data" on any table:
1. Click "Add Record"
2. Form fields are **auto-generated** based on column types:
   - String → Text input
   - Integer → Number input (step=1)
   - Float → Number input (step=any)
   - Boolean → Yes/No dropdown
   - Date → Date picker
   - DateTime → DateTime picker
   - JSON → JSON editor
3. Validations are enforced automatically
4. Edit/Delete records from table view

### 4. Use Advanced Filters (Static CRUD Examples)

Go to Projects/Users/Tags pages:
1. Click "Advanced Filters"
2. Add filter conditions:
   - Select field (e.g., `status`)
   - Choose operator (`eq`, `neq`, `like`, `in`, etc.)
   - Enter value
3. Chain multiple conditions with AND/OR logic
4. Click "Apply Filters"

**Filter Operators**:
- `eq` - Equals
- `neq` - Not equals
- `lt/lte` - Less than (or equal)
- `gt/gte` - Greater than (or equal)
- `like` - Pattern match (case-sensitive)
- `ilike` - Pattern match (case-insensitive)
- `in` - In list
- `nin` - Not in list
- `between` - Range
- `is_null` - Is NULL
- `is_not_null` - Is not NULL

## 🔧 API Endpoints

### App Management
- `POST /api/v1/apps/` - Create app
- `GET /api/v1/apps/` - List apps
- `GET /api/v1/apps/{id}` - Get app details
- `PUT /api/v1/apps/{id}` - Update app
- `DELETE /api/v1/apps/{id}` - Delete app

### Schema Management
- `POST /api/v1/schema/apps/{app_id}/tables` - Create table
- `GET /api/v1/schema/apps/{app_id}/tables` - List tables
- `GET /api/v1/schema/tables/{table_id}` - Get table details
- `PUT /api/v1/schema/tables/{table_id}` - Update table
- `DELETE /api/v1/schema/tables/{table_id}` - Delete table
- `POST /api/v1/schema/tables/{table_id}/columns` - Add column

### Dynamic Data CRUD
- `POST /api/v1/data/{table_name}` - Create record
- `GET /api/v1/data/{table_name}` - List records (paginated)
- `GET /api/v1/data/{table_name}/{record_id}` - Get record
- `PUT /api/v1/data/{table_name}/{record_id}` - Update record
- `DELETE /api/v1/data/{table_name}/{record_id}` - Delete record

Full API documentation: http://localhost:8000/docs

## 🎨 Features Implemented

### ✅ Meta-CRUD System
- [x] App Builder - Create applications with icons and colors
- [x] Table Designer - Visual table creator with 8 column types
- [x] Dynamic Data Manager - Auto-generated CRUD forms
- [x] Validation Engine - Required, unique, max_length, min/max, regex
- [x] JSON Storage - Flexible schema-less data storage
- [x] REST API - Complete CRUD endpoints for all resources

### ✅ Static CRUD Examples
- [x] Users Management - Full CRUD with role-based filtering
- [x] Projects Management - Status tracking, budget, priorities
- [x] Tags Management - Visual color picker, grid view
- [x] Advanced Filter Builder - 11 operators with AND/OR logic

### ✅ Dashboard System
- [x] Dashboard Engine - Execute metrics, charts, tables
- [x] 6 Aggregations - count, sum, avg, min, max, distinct_count
- [x] 4 Chart Types - bar, pie, line, donut

### 🔄 Coming Soon
- [ ] Dynamic Dashboard Generator - Auto-create dashboards from schemas
- [ ] Relationship Visualizer - ER diagram viewer
- [ ] Export/Import Schemas - JSON schema migration

## 🧪 Testing the System

### Test via UI (Recommended)

1. **Go to http://localhost:3000**
2. **Click "App Builder" in sidebar** (🔧 icon)
3. **Create a test app**:
   - Name: `test_crm`
   - Display Name: `Test CRM`
   - Pick any icon and color
4. **Click "Manage Tables"**
5. **Create a table**:
   - Name: `customers`
   - Add columns: name (string, required), email (string, required, unique), age (integer)
6. **Click "Manage Data"**
7. **Add records** - forms are auto-generated!

### Test via API

```bash
# 1. Create App
curl -X POST http://localhost:8000/api/v1/apps/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_app",
    "display_name": "Test App",
    "icon": "📦",
    "color": "#3B82F6",
    "is_active": true
  }'

# 2. Create Table
curl -X POST http://localhost:8000/api/v1/schema/apps/1/tables \
  -H "Content-Type: application/json" \
  -d '{
    "name": "customers",
    "display_name": "Customers",
    "columns": [
      {
        "name": "email",
        "display_name": "Email",
        "column_type": "string",
        "is_required": true,
        "is_unique": true,
        "max_length": 255
      }
    ]
  }'

# 3. Create Data
curl -X POST http://localhost:8000/api/v1/data/customers \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'

# 4. List Data
curl http://localhost:8000/api/v1/data/customers
```

## 📊 Database Schema

### Meta Tables (Dynamic CRUD Builder)
- `app` - Application definitions (name, icon, color)
- `table_schema` - Table metadata (name, display_name, app_id)
- `column_schema` - Column definitions (type, validations, constraints)
- `relationship_schema` - Table relationships (one-to-many, many-to-many)
- `dynamic_data` - Generic JSON storage for ALL dynamic table data

### Static Tables (Examples)
- `user` - User management
- `project` - Project tracking
- `tag` - Tag taxonomy
- `project_tag_link` - Many-to-many junction

## 🛠️ Development

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose up --build -d
```

### Access Database
```bash
docker-compose exec db psql -U postgres -d crud_db

# View tables
\dt

# View table schema
\d table_schema
\d column_schema
\d dynamic_data
```

## 🚦 Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common fixes:
docker-compose restart backend
```

### Frontend shows blank page
```bash
# Check logs
docker-compose logs frontend

# Rebuild frontend
docker-compose down
docker-compose up --build -d
```

### Database connection issues
```bash
# Check if DB is healthy
docker-compose ps

# Restart database
docker-compose restart db
```

### Reset Everything (Nuclear Option)
```bash
# WARNING: Deletes all data
docker-compose down -v
docker-compose up --build -d
docker-compose exec backend python seed_data.py
```

## 📈 What Makes This Special?

### 1. **Meta-CRUD Architecture**
Unlike traditional CRUD apps that have fixed models, this system lets users **define their own models at runtime**. Table schemas are stored as data, not code!

### 2. **Generic JSON Storage**
All dynamic table data is stored in a single `dynamic_data` table with a JSON column. This enables infinite flexibility without schema migrations.

### 3. **Type-Safe Validation**
Despite using JSON storage, we maintain type safety through our validation engine. Data is validated against column schemas before storage.

### 4. **Auto-Generated UI**
Forms are generated automatically based on table schemas. Add a column, get the input field for free!

### 5. **Production-Ready**
- Docker Compose orchestration
- Environment configuration
- Hot reload for development
- Health checks
- Error handling
- Pagination
- Input validation
- SQL injection protection (via SQLModel)

## 📄 Project Structure

```
backend/
├── models/schema_builder.py    # Meta-models (264 lines)
├── services/
│   ├── table_generator_service.py  # Schema + Data services (293 lines)
│   ├── filter_engine.py        # Query filtering
│   └── dashboard_engine.py     # Dashboard execution
├── routers/
│   ├── apps.py                 # App CRUD (120 lines)
│   ├── schema_builder.py       # Schema CRUD (170 lines)
│   ├── dynamic_data.py         # Data CRUD (130 lines)
│   └── [static examples]
└── main.py                     # FastAPI app with all routers

frontend/
├── pages/
│   └── AppBuilder.jsx          # App management (280 lines)
├── components/
│   ├── TableDesigner.jsx       # Table creator (540 lines)
│   └── DynamicDataManager.jsx  # Auto-CRUD forms (370 lines)
└── App.jsx                     # Router with /builder route
```

## 🎓 Learning Resources

This project demonstrates:
- **FastAPI** - Modern Python web framework
- **SQLModel** - Type-safe ORM
- **React Hooks** - useState, useEffect
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - JSON columns for flexible data
- **REST API Design** - Resource-based endpoints
- **Form Generation** - Dynamic UI from metadata
- **Validation Patterns** - Server-side + client-side

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:3000

## 🤝 Contributing

This is a demonstration project. Feel free to fork and extend!

## 📄 License

MIT License - use freely for any purpose

---

**Built with ❤️ using FastAPI, React, PostgreSQL, and Docker**

*System Status: ✅ All 8 tasks completed - fully functional meta-CRUD builder!*
