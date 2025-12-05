# System Architecture Diagram

## Component Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FRONTEND (React)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Dashboard Page                                           │  │
│  │  - MetricCard: Total Projects, Active, Budget            │  │
│  │  - ChartWidget: Bar/Pie/Line/Donut charts                │  │
│  │  - TableWidget: Filtered data tables                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Projects Page                                            │  │
│  │  - CRUD Table with advanced filters                      │  │
│  │  - Search, Sort, Paginate                                │  │
│  │  - Create/Edit/Delete forms                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Client (api.js)                                      │  │
│  │  - Axios HTTP client                                      │  │
│  │  - Projects/Users/Tags/Dashboards APIs                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API Calls
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                   http://localhost:8000                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API ROUTERS (FastAPI Endpoints)                         │  │
│  │                                                           │  │
│  │  /api/v1/users      - User CRUD operations               │  │
│  │  /api/v1/tags       - Tag CRUD operations                │  │
│  │  /api/v1/projects   - Project CRUD + advanced filters    │  │
│  │  /api/v1/dashboards - Dashboard execution                │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  BUSINESS LOGIC SERVICES                                  │  │
│  │                                                           │  │
│  │  UserService:                                             │  │
│  │    - validate_user()                                      │  │
│  │    - before_create() / after_create()                     │  │
│  │    - before_update() / after_update()                     │  │
│  │    - before_delete() / after_delete()                     │  │
│  │    - enrich() (computed fields)                           │  │
│  │                                                           │  │
│  │  ProjectService:                                          │  │
│  │    - validate_project()                                   │  │
│  │    - hooks: before/after create/update/delete             │  │
│  │    - enrich: total_tags, is_overdue                       │  │
│  │                                                           │  │
│  │  TagService:                                              │  │
│  │    - validate_tag()                                       │  │
│  │    - hooks and computed fields                            │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  ADVANCED FILTER ENGINE                                   │  │
│  │                                                           │  │
│  │  QueryBuilder:                                            │  │
│  │    - apply_simple_filters()                               │  │
│  │      • eq, neq, lt, lte, gt, gte                          │  │
│  │      • like, ilike, in, nin, between                      │  │
│  │                                                           │  │
│  │    - apply_json_filters()                                 │  │
│  │      • AND/OR logic groups                                │  │
│  │      • Nested conditions                                  │  │
│  │                                                           │  │
│  │    - apply_sorting()                                      │  │
│  │      • Multi-field sort (asc/desc)                        │  │
│  │                                                           │  │
│  │    - apply_pagination()                                   │  │
│  │      • Page-based navigation                              │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  DASHBOARD ENGINE                                         │  │
│  │                                                           │  │
│  │  DashboardEngine:                                         │  │
│  │    - run_widget()                                         │  │
│  │                                                           │  │
│  │    Widget Types:                                          │  │
│  │      • Metric: count, sum, avg, min, max                  │  │
│  │      • Chart: bar, pie, line, donut                       │  │
│  │      • Table: filtered & paginated data                   │  │
│  │                                                           │  │
│  │    Aggregations:                                          │  │
│  │      • GROUP BY dimensions                                │  │
│  │      • COUNT, SUM, AVG, MIN, MAX                          │  │
│  │      • DISTINCT COUNT                                     │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  MODELS (SQLModel)                                        │  │
│  │                                                           │  │
│  │  User:                                                    │  │
│  │    - id, email, full_name, role, is_active                │  │
│  │    - hashed_password, created_at, updated_at              │  │
│  │    - projects (relationship)                              │  │
│  │                                                           │  │
│  │  Tag:                                                     │  │
│  │    - id, name, color, description                         │  │
│  │    - created_at                                           │  │
│  │    - projects (many-to-many)                              │  │
│  │                                                           │  │
│  │  Project:                                                 │  │
│  │    - id, name, description, status, priority              │  │
│  │    - budget, start_date, end_date                         │  │
│  │    - owner_id (FK), created_at, updated_at                │  │
│  │    - owner (relationship), tags (many-to-many)            │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               │ SQL Queries
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    PostgreSQL Database                            │
│                     localhost:5432                                │
│                                                                   │
│  Tables:                                                          │
│    - user                                                         │
│    - tag                                                          │
│    - project                                                      │
│    - projecttaglink (many-to-many)                                │
│                                                                   │
│  Indexes:                                                         │
│    - user.email (unique)                                          │
│    - tag.name (unique)                                            │
│    - project.name                                                 │
│                                                                   │
│  Volume: postgres_data (persistent)                               │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow Example: Create Project

```
1. User clicks "Create Project" in React UI
                  ↓
2. Form submits data to Frontend API client
                  ↓
3. POST /api/v1/projects
   Body: {name, description, status, priority, owner_id, tag_ids}
                  ↓
4. Router receives request → projects.py
                  ↓
5. ProjectService.before_create()
   - Validates name length
   - Validates priority range (1-5)
   - Validates status enum
   - Validates dates
   - Validates budget
                  ↓
6. Create Project record in database
                  ↓
7. ProjectService.after_create()
   - Attach tags via tag_ids
   - Log audit trail
                  ↓
8. ProjectService.enrich()
   - Calculate total_tags
   - Calculate is_overdue
                  ↓
9. Return ProjectRead response
                  ↓
10. Frontend receives response → updates UI
```

## Filter Flow Example: Complex Query

```
User applies filter: "High priority projects in progress"
                  ↓
POST /api/v1/projects/filter
Body: {
  "logic": "and",
  "filters": [
    {"field": "priority", "op": "gte", "value": 4},
    {"field": "status", "op": "eq", "value": "in_progress"}
  ]
}
                  ↓
Router → QueryBuilder.apply_json_filters()
                  ↓
Build SQL query:
  SELECT * FROM project
  WHERE priority >= 4
    AND status = 'in_progress'
                  ↓
Execute query → Return results
                  ↓
Enrich each project with computed fields
                  ↓
Return paginated response
```

## Dashboard Flow Example: Execute Widget

```
User views dashboard → Frontend loads widgets
                  ↓
POST /api/v1/dashboards/widget
Body: {
  "type": "chart",
  "chart_type": "bar",
  "title": "Projects by Status",
  "query": {
    "resource": "project",
    "group_by": "status",
    "aggregate": "count"
  }
}
                  ↓
Router → DashboardEngine.run_widget()
                  ↓
Execute aggregation query:
  SELECT status, COUNT(*) as count
  FROM project
  GROUP BY status
                  ↓
Format results:
  [
    {"label": "open", "value": 5},
    {"label": "in_progress", "value": 3},
    {"label": "completed", "value": 2}
  ]
                  ↓
Return widget data → Frontend renders chart
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│  FRONTEND LAYER                             │
│  - React 18 (UI Components)                 │
│  - Vite (Build Tool)                        │
│  - Tailwind CSS (Styling)                   │
│  - Recharts (Data Visualization)            │
│  - Axios (HTTP Client)                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  API LAYER                                  │
│  - FastAPI 0.109 (Web Framework)            │
│  - Uvicorn (ASGI Server)                    │
│  - Pydantic (Data Validation)               │
│  - OpenAPI/Swagger (Documentation)          │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER                       │
│  - Service Classes                          │
│  - Validation Rules                         │
│  - Pre/Post Hooks                           │
│  - Computed Fields                          │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  DATA ACCESS LAYER                          │
│  - SQLModel (ORM)                            │
│  - Filter Engine                            │
│  - Dashboard Engine                         │
│  - Query Builder                            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  DATABASE LAYER                             │
│  - PostgreSQL 15                            │
│  - psycopg2 (Driver)                        │
│  - Persistent Volume                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  INFRASTRUCTURE LAYER                       │
│  - Docker Containers                        │
│  - Docker Compose                           │
│  - Networking                               │
│  - Volume Management                        │
└─────────────────────────────────────────────┘
```

## Port Mapping

```
┌────────────────────┐
│   Host Machine     │
│                    │
│  :3000 ────────┐   │
│  :8000 ────┐   │   │
│  :5432 ──┐ │   │   │
└──────────┼─┼───┼───┘
           │ │   │
           │ │   │   Docker Network: crud_network
┌──────────┼─┼───┼───────────────────────────────┐
│          │ │   │                               │
│  ┌───────▼─────────┐  ┌──────────────────┐    │
│  │   Frontend      │  │   PostgreSQL     │    │
│  │   Container     │  │   Container      │    │
│  │   :3000        │  │   :5432         │    │
│  └─────────────────┘  └──────────────────┘    │
│          │                                     │
│          │                                     │
│  ┌───────▼─────────┐                          │
│  │   Backend       │                          │
│  │   Container     │                          │
│  │   :8000        │                          │
│  └─────────────────┘                          │
│                                                │
└────────────────────────────────────────────────┘
```
