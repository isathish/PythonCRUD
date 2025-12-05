# API Testing Examples

All examples use `http://localhost:8000` as the base URL.

## 1. Users API

### Create User
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "role": "user",
    "password": "securepass123"
  }'
```

### List Users (with filters)
```bash
# Get all users
curl http://localhost:8000/api/v1/users

# Filter by role
curl "http://localhost:8000/api/v1/users?role__eq=admin"

# Search by name (case-insensitive)
curl "http://localhost:8000/api/v1/users?full_name__ilike=john"

# Get active users only
curl "http://localhost:8000/api/v1/users?is_active=true"

# Pagination
curl "http://localhost:8000/api/v1/users?page=1&limit=10"

# Sort by name
curl "http://localhost:8000/api/v1/users?sort=full_name:asc"
```

### Get Single User
```bash
curl http://localhost:8000/api/v1/users/1
```

### Update User
```bash
curl -X PATCH http://localhost:8000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name",
    "role": "admin"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/v1/users/1
```

---

## 2. Tags API

### Create Tag
```bash
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend",
    "color": "#3b82f6",
    "description": "Backend development tasks"
  }'
```

### List Tags
```bash
# Get all tags
curl http://localhost:8000/api/v1/tags

# Search by name
curl "http://localhost:8000/api/v1/tags?name__ilike=back"

# Filter by color
curl "http://localhost:8000/api/v1/tags?color__eq=%233b82f6"
```

### Update Tag
```bash
curl -X PATCH http://localhost:8000/api/v1/tags/1 \
  -H "Content-Type: application/json" \
  -d '{
    "color": "#ff0000"
  }'
```

---

## 3. Projects API

### Create Project
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Platform",
    "description": "Build new e-commerce system",
    "status": "in_progress",
    "priority": 5,
    "budget": 100000,
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "owner_id": 1,
    "tag_ids": [1, 2]
  }'
```

### List Projects (Simple Filters)
```bash
# Get all projects
curl http://localhost:8000/api/v1/projects

# Filter by status
curl "http://localhost:8000/api/v1/projects?status__eq=in_progress"

# Filter by multiple statuses
curl "http://localhost:8000/api/v1/projects?status__in=open,in_progress"

# High priority projects (>=4)
curl "http://localhost:8000/api/v1/projects?priority__gte=4"

# Search by name
curl "http://localhost:8000/api/v1/projects?name__ilike=commerce"

# Filter by budget range
curl "http://localhost:8000/api/v1/projects?budget__gte=50000&budget__lte=150000"

# Filter by owner
curl "http://localhost:8000/api/v1/projects?owner_id__eq=1"

# Sort by priority (descending)
curl "http://localhost:8000/api/v1/projects?sort=priority:desc,name:asc"

# Pagination
curl "http://localhost:8000/api/v1/projects?page=1&limit=5"
```

### Complex Filtering (JSON)
```bash
# Projects that are (status=open) AND (priority>=4 OR name contains "critical")
curl -X POST http://localhost:8000/api/v1/projects/filter \
  -H "Content-Type: application/json" \
  -d '{
    "logic": "and",
    "filters": [
      {"field": "status", "op": "eq", "value": "in_progress"},
      {
        "logic": "or",
        "filters": [
          {"field": "priority", "op": "gte", "value": 4},
          {"field": "name", "op": "ilike", "value": "critical"}
        ]
      }
    ]
  }'

# High budget AND (high priority OR in progress)
curl -X POST http://localhost:8000/api/v1/projects/filter \
  -H "Content-Type: application/json" \
  -d '{
    "logic": "and",
    "filters": [
      {"field": "budget", "op": "gte", "value": 50000},
      {
        "logic": "or",
        "filters": [
          {"field": "priority", "op": "eq", "value": 5},
          {"field": "status", "op": "eq", "value": "in_progress"}
        ]
      }
    ]
  }'
```

### Update Project
```bash
curl -X PATCH http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": 3,
    "tag_ids": [1, 2, 3]
  }'
```

### Delete Project
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/1
```

---

## 4. Dashboard API

### List All Dashboards
```bash
curl http://localhost:8000/api/v1/dashboards
```

### Get Dashboard Definition
```bash
curl http://localhost:8000/api/v1/dashboards/project_summary
```

### Execute Dashboard
```bash
# Execute predefined Project Summary dashboard
curl http://localhost:8000/api/v1/dashboards/project_summary/execute

# Execute User Summary dashboard
curl http://localhost:8000/api/v1/dashboards/user_summary/execute
```

### Run Single Widget - Metric
```bash
# Count total projects
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "metric",
    "title": "Total Projects",
    "query": {
      "resource": "project",
      "aggregate": "count"
    }
  }'

# Sum of all budgets
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "metric",
    "title": "Total Budget",
    "query": {
      "resource": "project",
      "aggregate": "sum",
      "field": "budget"
    }
  }'

# Average priority
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "metric",
    "title": "Average Priority",
    "query": {
      "resource": "project",
      "aggregate": "avg",
      "field": "priority"
    }
  }'
```

### Run Single Widget - Chart
```bash
# Bar chart: Projects by status
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "chart",
    "chart_type": "bar",
    "title": "Projects by Status",
    "query": {
      "resource": "project",
      "group_by": "status",
      "aggregate": "count"
    }
  }'

# Pie chart: Projects by priority
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "chart",
    "chart_type": "pie",
    "title": "Projects by Priority",
    "query": {
      "resource": "project",
      "group_by": "priority",
      "aggregate": "count"
    }
  }'

# Donut chart: Users by role
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "chart",
    "chart_type": "donut",
    "title": "Users by Role",
    "query": {
      "resource": "user",
      "group_by": "role",
      "aggregate": "count"
    }
  }'
```

### Run Single Widget - Table
```bash
# High priority projects
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Active projects
curl -X POST http://localhost:8000/api/v1/dashboards/widget \
  -H "Content-Type: application/json" \
  -d '{
    "type": "table",
    "title": "Active Projects",
    "query": {
      "resource": "project",
      "filters": {
        "status__in": "open,in_progress"
      },
      "limit": 20
    }
  }'
```

### Run Custom Dashboard
```bash
curl -X POST http://localhost:8000/api/v1/dashboards/run \
  -H "Content-Type: application/json" \
  -d '{
    "widgets": [
      {
        "type": "metric",
        "title": "Total Projects",
        "query": {
          "resource": "project",
          "aggregate": "count"
        }
      },
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
    ]
  }'
```

---

## 5. Advanced Query Examples

### Comparison Operators

```bash
# Equal
curl "http://localhost:8000/api/v1/projects?status__eq=open"

# Not equal
curl "http://localhost:8000/api/v1/projects?status__neq=archived"

# Less than
curl "http://localhost:8000/api/v1/projects?priority__lt=3"

# Less than or equal
curl "http://localhost:8000/api/v1/projects?budget__lte=50000"

# Greater than
curl "http://localhost:8000/api/v1/projects?priority__gt=3"

# Greater than or equal
curl "http://localhost:8000/api/v1/projects?priority__gte=4"

# LIKE (case-sensitive)
curl "http://localhost:8000/api/v1/projects?name__like=Project"

# ILIKE (case-insensitive)
curl "http://localhost:8000/api/v1/projects?name__ilike=project"

# IN list
curl "http://localhost:8000/api/v1/projects?status__in=open,in_progress"

# NOT IN list
curl "http://localhost:8000/api/v1/projects?status__nin=archived,completed"

# BETWEEN
curl "http://localhost:8000/api/v1/projects?budget__between=10000,50000"
```

### Combined Filters

```bash
# Multiple filters (AND logic)
curl "http://localhost:8000/api/v1/projects?status__eq=in_progress&priority__gte=4&budget__gte=50000"

# With sorting and pagination
curl "http://localhost:8000/api/v1/projects?status__in=open,in_progress&sort=priority:desc,name:asc&page=1&limit=10"
```

---

## 6. Health Check

```bash
curl http://localhost:8000/health
```

---

## Testing Script

Save this as `test_api.sh` and run it:

```bash
#!/bin/bash

API_URL="http://localhost:8000/api/v1"

echo "Testing CRUD API..."

# Create User
echo "\n1. Creating user..."
USER_ID=$(curl -s -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","role":"user","password":"test123"}' \
  | jq -r '.id')
echo "Created user with ID: $USER_ID"

# Create Tag
echo "\n2. Creating tag..."
TAG_ID=$(curl -s -X POST $API_URL/tags \
  -H "Content-Type: application/json" \
  -d '{"name":"TestTag","color":"#ff0000"}' \
  | jq -r '.id')
echo "Created tag with ID: $TAG_ID"

# Create Project
echo "\n3. Creating project..."
PROJECT_ID=$(curl -s -X POST $API_URL/projects \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test Project\",\"status\":\"open\",\"priority\":5,\"owner_id\":$USER_ID,\"tag_ids\":[$TAG_ID]}" \
  | jq -r '.id')
echo "Created project with ID: $PROJECT_ID"

# List Projects
echo "\n4. Listing projects..."
curl -s "$API_URL/projects" | jq '.data | length'

# Execute Dashboard
echo "\n5. Executing dashboard..."
curl -s "$API_URL/dashboards/project_summary/execute" | jq '.results | length'

echo "\n✅ All tests completed!"
```
