# 🚀 Quick Start Guide

## Step 1: Start Docker Desktop

1. Open **Docker Desktop** application on your Mac
2. Wait until Docker is fully running (whale icon in menu bar should be stable)
3. Verify Docker is running:
   ```bash
   docker --version
   docker ps
   ```

## Step 2: Start the Application

Option A - Using the script:
```bash
cd /Users/sathishkumarn/RnD/Github/PythonCRUD
./start.sh
```

Option B - Manual start:
```bash
cd /Users/sathishkumarn/RnD/Github/PythonCRUD
docker-compose up -d --build
```

## Step 3: Wait for Services to Start

This will take 2-3 minutes on first run as Docker builds the images.

Check status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

## Step 4: Access the Application

Once all services are running:

- **Frontend (React)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

## Step 5: Create Test Data

Open http://localhost:8000/docs and use the Swagger UI to:

1. Create a User:
   - Go to `POST /api/v1/users`
   - Click "Try it out"
   - Use this data:
   ```json
   {
     "email": "admin@example.com",
     "full_name": "Admin User",
     "role": "admin",
     "password": "admin123"
   }
   ```

2. Create Tags:
   - Go to `POST /api/v1/tags`
   - Create tags like "Backend", "Frontend", "DevOps"

3. Create Projects:
   - Go to `POST /api/v1/projects`
   - Create projects with different priorities and statuses

## Step 6: Explore Features

### Frontend Dashboard
- Navigate to http://localhost:3000
- View the Project Summary dashboard with metrics and charts
- Click on "Projects" to see the CRUD table with filters
- Test the advanced filters

### Backend API
- Open http://localhost:8000/docs
- Try different filter combinations
- Test the dashboard endpoints

## Common Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec db psql -U postgres -d cruddb
```

## Troubleshooting

### Docker not starting?
- Ensure Docker Desktop is installed
- Check if port 5432, 8000, or 3000 are already in use
- Restart Docker Desktop

### Backend failing to start?
```bash
docker-compose logs backend
```
Common issues:
- Database not ready yet (wait 30 seconds and check again)
- Port 8000 already in use

### Frontend failing to start?
```bash
docker-compose logs frontend
```
Common issues:
- npm install taking time (wait 2-3 minutes)
- Port 3000 already in use

### Cannot connect to database?
```bash
docker-compose exec db psql -U postgres -d cruddb
```
If this works, the database is running correctly.

## Testing the System

### Test 1: Create Data via API

```bash
# Create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "role": "user",
    "password": "test123"
  }'

# Create tag
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Important", "color": "#ff0000"}'

# Create project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "Testing the system",
    "status": "open",
    "priority": 5,
    "budget": 10000,
    "owner_id": 1,
    "tag_ids": [1]
  }'
```

### Test 2: Test Filtering

```bash
# Get high priority projects
curl "http://localhost:8000/api/v1/projects?priority__gte=4"

# Search by name
curl "http://localhost:8000/api/v1/projects?name__ilike=test"

# Get open projects
curl "http://localhost:8000/api/v1/projects?status__eq=open"
```

### Test 3: Test Dashboard

```bash
# Get dashboard list
curl http://localhost:8000/api/v1/dashboards

# Execute project summary dashboard
curl http://localhost:8000/api/v1/dashboards/project_summary/execute
```

## Next Steps

1. ✅ Start Docker Desktop
2. ✅ Run `./start.sh` or `docker-compose up -d --build`
3. ✅ Wait for services to start (check logs)
4. ✅ Open http://localhost:3000
5. ✅ Create test data via API docs
6. ✅ Explore the dashboard and CRUD features

## Need Help?

Check the full README.md for:
- Complete API documentation
- Architecture details
- Advanced features
- Production deployment guide
