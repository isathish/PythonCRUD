# Advanced CRUD System with Business Logic & Dashboard Builder

A production-grade CRUD system built with FastAPI, PostgreSQL, and React featuring:

✅ **Business Logic Layer** with validation, hooks, and computed fields  
✅ **Advanced Filter Engine** with comparison operators, AND/OR logic, relationship filters  
✅ **Dashboard Builder** with metrics, charts, tables, and aggregations  
✅ **Complete CRUD Operations** for Projects, Users, and Tags  
✅ **Docker Compose** setup for easy deployment

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  - Dashboard Builder UI                                      │
│  - CRUD Tables with Advanced Filtering                      │
│  - Chart Components (Bar, Pie, Line, Donut)                 │
│  - Drag & Drop Layout Support                               │
└─────────────────────────────────────────────────────────────┘
                            ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Business Logic Layer                                │   │
│  │  - Validation Rules                                  │   │
│  │  - Pre/Post Hooks (create, update, delete)          │   │
│  │  - Computed Fields                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Advanced Filter Engine                              │   │
│  │  - Comparison Ops (eq, neq, lt, lte, gt, gte, like) │   │
│  │  - Logical Ops (AND/OR groups)                       │   │
│  │  - Relationship Filters                              │   │
│  │  - Sorting & Pagination                              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Dashboard Engine                                    │   │
│  │  - Metric Widgets                                    │   │
│  │  - Chart Widgets (aggregations, group by)           │   │
│  │  - Table Widgets (filtered data)                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                        │
│  - Users, Projects, Tags                                     │
│  - Relationships & Indexes                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Git

### Installation & Run

1. **Clone the repository:**
   ```bash
   cd /Users/sathishkumarn/RnD/Github/PythonCRUD
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Start all services:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - **Frontend:** http://localhost:3000
   - **Backend API:** http://localhost:8000
   - **API Docs:** http://localhost:8000/docs
   - **PostgreSQL:** localhost:5432

5. **View logs:**
   ```bash
   docker-compose logs -f
   ```

6. **Stop services:**
   ```bash
   docker-compose down
   ```

---

## 📊 Features

### 1. Business Logic Layer

Every model has a **Service Layer** with:

#### **Validation Rules**
```python
# Example: ProjectService
def validate_project(data, session):
    if len(data.name) < 3:
        raise ValueError("Project name too short")
    if data.priority < 1 or data.priority > 5:
        raise ValueError("Priority must be 1-5")
```

#### **Pre/Post Hooks**
```python
before_create()   # Validate before creation
after_create()    # Log audit trail, send notifications
before_update()   # Validate updates
after_update()    # Update related records
before_delete()   # Check dependencies
after_delete()    # Cleanup operations
```

#### **Computed Fields**
```python
# Automatically calculated fields
project.total_tags      # Count of associated tags
project.is_overdue      # Boolean based on end_date
user.project_count      # Count of user's projects
```

---

### 2. Advanced Filter Engine

#### **Comparison Operators**

| Operator | Example | Description |
|----------|---------|-------------|
| `eq` | `status__eq=open` | Equals |
| `neq` | `status__neq=archived` | Not equals |
| `lt` | `priority__lt=3` | Less than |
| `lte` | `budget__lte=1000` | Less than or equal |
| `gt` | `priority__gt=2` | Greater than |
| `gte` | `priority__gte=4` | Greater than or equal |
| `like` | `name__like=Project` | SQL LIKE (case-sensitive) |
| `ilike` | `name__ilike=project` | SQL ILIKE (case-insensitive) |
| `in` | `status__in=open,closed` | IN list |
| `nin` | `status__nin=archived` | NOT IN list |
| `between` | `date__between=2024-01-01,2024-12-31` | BETWEEN range |

#### **Simple Filtering (GET requests)**
```bash
# Filter projects by status and priority
GET /api/v1/projects?status__eq=open&priority__gte=4

# Search by name (case-insensitive)
GET /api/v1/projects?name__ilike=critical

# Multiple filters
GET /api/v1/projects?status__in=open,in_progress&priority__gte=3
```

#### **Complex JSON Filters (POST requests)**
```bash
POST /api/v1/projects/filter
{
  "logic": "and",
  "filters": [
    {"field": "status", "op": "eq", "value": "open"},
    {
      "logic": "or",
      "filters": [
        {"field": "priority", "op": "gte", "value": 4},
        {"field": "name", "op": "ilike", "value": "critical"}
      ]
    }
  ]
}
```

#### **Sorting**
```bash
# Sort by priority descending, then name ascending
GET /api/v1/projects?sort=priority:desc,name:asc
```

#### **Pagination**
```bash
GET /api/v1/projects?page=1&limit=20
```

---

### 3. Dashboard Builder

#### **Pre-built Dashboards**

**Project Summary Dashboard:**
- Total Projects (metric)
- Active Projects (metric)
- Total Budget (metric)
- Average Priority (metric)
- Projects by Status (bar chart)
- Projects by Priority (pie chart)
- High Priority Projects (table)

**User Summary Dashboard:**
- Total Users (metric)
- Active Users (metric)
- Users by Role (donut chart)

#### **Dashboard API Endpoints**

```bash
# List all dashboards
GET /api/v1/dashboards

# Get dashboard definition
GET /api/v1/dashboards/{dashboard_id}

# Execute dashboard (runs all widgets)
GET /api/v1/dashboards/{dashboard_id}/execute

# Run custom widget
POST /api/v1/dashboards/widget
{
  "type": "chart",
  "chart_type": "bar",
  "title": "Projects by Status",
  "query": {
    "resource": "project",
    "group_by": "status",
    "aggregate": "count"
  }
}
```

#### **Widget Types**

**1. Metric Widget**
```json
{
  "type": "metric",
  "title": "Total Projects",
  "query": {
    "resource": "project",
    "aggregate": "count"
  }
}
```

**2. Chart Widget**
```json
{
  "type": "chart",
  "chart_type": "bar",  // bar, pie, line, donut
  "title": "Projects by Status",
  "query": {
    "resource": "project",
    "group_by": "status",
    "aggregate": "count"
  }
}
```

**3. Table Widget**
```json
{
  "type": "table",
  "title": "High Priority Projects",
  "query": {
    "resource": "project",
    "filters": {
      "priority__gte": "4"
    },
    "sort": "priority:desc",
    "limit": 10
  }
}
```

#### **Supported Aggregations**

- `count` - Count records
- `sum` - Sum numeric field
- `avg` - Average of numeric field
- `min` - Minimum value
- `max` - Maximum value
- `distinct_count` - Count distinct values

---

## 🔌 API Endpoints

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects (with filters)
- `GET /api/v1/projects/{id}` - Get project
- `PATCH /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/filter` - Advanced filtering

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users (with filters)
- `GET /api/v1/users/{id}` - Get user
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Tags
- `POST /api/v1/tags` - Create tag
- `GET /api/v1/tags` - List tags (with filters)
- `GET /api/v1/tags/{id}` - Get tag
- `PATCH /api/v1/tags/{id}` - Update tag
- `DELETE /api/v1/tags/{id}` - Delete tag

### Dashboards
- `GET /api/v1/dashboards` - List dashboards
- `GET /api/v1/dashboards/{id}` - Get dashboard
- `GET /api/v1/dashboards/{id}/execute` - Execute dashboard
- `POST /api/v1/dashboards/widget` - Run single widget
- `POST /api/v1/dashboards/run` - Run custom dashboard

---

## 📁 Project Structure

```
PythonCRUD/
├── backend/
│   ├── core/
│   │   ├── config.py           # Configuration
│   │   └── database.py         # Database setup
│   ├── models/
│   │   ├── user.py             # User model & schemas
│   │   ├── tag.py              # Tag model & schemas
│   │   └── project.py          # Project model & schemas
│   ├── services/
│   │   ├── user_service.py     # User business logic
│   │   ├── tag_service.py      # Tag business logic
│   │   ├── project_service.py  # Project business logic
│   │   ├── filter_engine.py    # Advanced filtering
│   │   └── dashboard_engine.py # Dashboard execution
│   ├── routers/
│   │   ├── users.py            # User endpoints
│   │   ├── tags.py             # Tag endpoints
│   │   ├── projects.py         # Project endpoints
│   │   └── dashboards.py       # Dashboard endpoints
│   ├── dashboards/
│   │   └── schema.json         # Dashboard definitions
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js          # API client
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   └── dashboard/
│   │   │       ├── MetricCard.jsx
│   │   │       ├── ChartWidget.jsx
│   │   │       └── TableWidget.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   └── ProjectsPage.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🛠️ Development

### Backend Development

```bash
# Enter backend container
docker-compose exec backend bash

# Run tests (if implemented)
pytest

# Check logs
docker-compose logs -f backend
```

### Frontend Development

```bash
# Enter frontend container
docker-compose exec frontend sh

# Install new package
npm install package-name

# Check logs
docker-compose logs -f frontend
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d cruddb

# View tables
\dt

# Query data
SELECT * FROM project;
```

---

## 🧪 Testing the API

### Create Test Data

```bash
# Create a user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "admin",
    "password": "securepass123"
  }'

# Create a tag
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend",
    "color": "#3b82f6",
    "description": "Backend development"
  }'

# Create a project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Platform",
    "description": "Build new e-commerce system",
    "status": "in_progress",
    "priority": 5,
    "budget": 50000,
    "owner_id": 1,
    "tag_ids": [1]
  }'
```

### Test Filtering

```bash
# Filter high priority projects
curl "http://localhost:8000/api/v1/projects?priority__gte=4"

# Search projects
curl "http://localhost:8000/api/v1/projects?name__ilike=commerce"

# Complex filter with JSON
curl -X POST http://localhost:8000/api/v1/projects/filter \
  -H "Content-Type: application/json" \
  -d '{
    "logic": "and",
    "filters": [
      {"field": "status", "op": "eq", "value": "in_progress"},
      {"field": "priority", "op": "gte", "value": 3}
    ]
  }'
```

### Test Dashboard

```bash
# Execute project summary dashboard
curl http://localhost:8000/api/v1/dashboards/project_summary/execute
```

---

## 🔐 Security Notes

- Change `SECRET_KEY` in `.env` for production
- Implement authentication (JWT) for production use
- Use HTTPS in production
- Set strong database passwords
- Implement rate limiting
- Add input sanitization

---

## 🚢 Production Deployment

1. **Update environment variables**
2. **Enable HTTPS**
3. **Use production database**
4. **Set up monitoring**
5. **Configure backup strategy**
6. **Implement proper authentication**
7. **Add rate limiting**
8. **Enable logging**

---

## 📈 Future Enhancements

- [ ] Authentication & Authorization (JWT)
- [ ] Real-time updates (WebSockets)
- [ ] Export dashboards (PDF, Excel)
- [ ] Custom dashboard builder UI
- [ ] Role-based access control (RBAC)
- [ ] Audit logging
- [ ] Email notifications
- [ ] File uploads
- [ ] Advanced analytics
- [ ] Multi-tenancy

---

## 🤝 Contributing

This is a demonstration project showcasing production-grade CRUD architecture. Feel free to use it as a template for your own projects.

---

## 📝 License

MIT License - feel free to use for commercial or personal projects.

---

## 📞 Support

For issues or questions, please check:
- Backend API Docs: http://localhost:8000/docs
- Docker logs: `docker-compose logs`
- GitHub Issues (if applicable)

---

**Built with ❤️ using FastAPI, PostgreSQL, React, and Docker**
