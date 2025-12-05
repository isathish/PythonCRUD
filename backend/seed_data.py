"""
Seed script to populate database with sample data
Run: docker-compose exec backend python seed_data.py
"""
from sqlmodel import Session, select
from core.database import engine
from models.user import User
from models.tag import Tag
from models.project import Project, ProjectTagLink
import bcrypt
from datetime import date, timedelta

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    with Session(engine) as session:
        print("🌱 Starting data seeding...")
        
        # Check if data already exists
        existing_users = session.exec(select(User)).first()
        if existing_users:
            print("⚠️  Data already exists. Skipping seed.")
            return
        
        # Create Users
        print("👥 Creating users...")
        users = [
            User(
                email="admin@example.com",
                full_name="Admin User",
                role="admin",
                hashed_password=hash_password("admin123"),
                is_active=True
            ),
            User(
                email="john@example.com",
                full_name="John Doe",
                role="user",
                hashed_password=hash_password("password123"),
                is_active=True
            ),
            User(
                email="jane@example.com",
                full_name="Jane Smith",
                role="user",
                hashed_password=hash_password("password123"),
                is_active=True
            ),
            User(
                email="bob@example.com",
                full_name="Bob Johnson",
                role="viewer",
                hashed_password=hash_password("password123"),
                is_active=True
            ),
        ]
        for user in users:
            session.add(user)
        session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create Tags
        print("🏷️  Creating tags...")
        tags = [
            Tag(name="Backend", color="#3b82f6", description="Backend development tasks"),
            Tag(name="Frontend", color="#10b981", description="Frontend development tasks"),
            Tag(name="DevOps", color="#f59e0b", description="DevOps and infrastructure"),
            Tag(name="Urgent", color="#ef4444", description="High priority items"),
            Tag(name="Bug", color="#dc2626", description="Bug fixes"),
            Tag(name="Feature", color="#8b5cf6", description="New features"),
            Tag(name="Documentation", color="#6366f1", description="Documentation tasks"),
            Tag(name="Testing", color="#ec4899", description="Testing related"),
        ]
        for tag in tags:
            session.add(tag)
        session.commit()
        print(f"✅ Created {len(tags)} tags")
        
        # Refresh to get IDs
        for user in users:
            session.refresh(user)
        for tag in tags:
            session.refresh(tag)
        
        # Create Projects
        print("📁 Creating projects...")
        projects_data = [
            {
                "name": "E-commerce Platform",
                "description": "Build a modern e-commerce platform with React and FastAPI",
                "status": "in_progress",
                "priority": 9,
                "budget": 150000.0,
                "start_date": date.today() - timedelta(days=30),
                "end_date": date.today() + timedelta(days=60),
                "owner_id": users[1].id,
                "tag_names": ["Frontend", "Backend", "Urgent"]
            },
            {
                "name": "Mobile App Development",
                "description": "Develop iOS and Android apps for the platform",
                "status": "planning",
                "priority": 7,
                "budget": 80000.0,
                "start_date": date.today() + timedelta(days=15),
                "end_date": date.today() + timedelta(days=120),
                "owner_id": users[2].id,
                "tag_names": ["Frontend", "Feature"]
            },
            {
                "name": "CI/CD Pipeline Setup",
                "description": "Configure automated deployment pipeline",
                "status": "completed",
                "priority": 8,
                "budget": 25000.0,
                "start_date": date.today() - timedelta(days=60),
                "end_date": date.today() - timedelta(days=10),
                "owner_id": users[1].id,
                "tag_names": ["DevOps"]
            },
            {
                "name": "API Documentation",
                "description": "Create comprehensive API documentation",
                "status": "in_progress",
                "priority": 5,
                "budget": 15000.0,
                "start_date": date.today() - timedelta(days=5),
                "end_date": date.today() + timedelta(days=20),
                "owner_id": users[3].id,
                "tag_names": ["Documentation", "Backend"]
            },
            {
                "name": "User Authentication Bug Fix",
                "description": "Fix critical authentication bypass vulnerability",
                "status": "on_hold",
                "priority": 10,
                "budget": 5000.0,
                "start_date": date.today() - timedelta(days=2),
                "end_date": date.today() + timedelta(days=3),
                "owner_id": users[1].id,
                "tag_names": ["Bug", "Urgent", "Backend"]
            },
            {
                "name": "Performance Testing",
                "description": "Conduct load testing and optimize performance",
                "status": "planning",
                "priority": 6,
                "budget": 30000.0,
                "start_date": date.today() + timedelta(days=30),
                "end_date": date.today() + timedelta(days=50),
                "owner_id": users[2].id,
                "tag_names": ["Testing", "DevOps"]
            },
            {
                "name": "Payment Gateway Integration",
                "description": "Integrate Stripe payment processing",
                "status": "in_progress",
                "priority": 9,
                "budget": 45000.0,
                "start_date": date.today() - timedelta(days=10),
                "end_date": date.today() + timedelta(days=25),
                "owner_id": users[1].id,
                "tag_names": ["Backend", "Feature", "Urgent"]
            },
            {
                "name": "Admin Dashboard",
                "description": "Build admin control panel with analytics",
                "status": "planning",
                "priority": 7,
                "budget": 60000.0,
                "start_date": date.today() + timedelta(days=5),
                "end_date": date.today() + timedelta(days=45),
                "owner_id": users[2].id,
                "tag_names": ["Frontend", "Feature"]
            },
            {
                "name": "Database Migration",
                "description": "Migrate from MySQL to PostgreSQL",
                "status": "completed",
                "priority": 8,
                "budget": 20000.0,
                "start_date": date.today() - timedelta(days=90),
                "end_date": date.today() - timedelta(days=70),
                "owner_id": users[1].id,
                "tag_names": ["Backend", "DevOps"]
            },
            {
                "name": "Security Audit",
                "description": "Complete security assessment and penetration testing",
                "status": "cancelled",
                "priority": 6,
                "budget": 35000.0,
                "start_date": date.today() - timedelta(days=20),
                "end_date": date.today() - timedelta(days=5),
                "owner_id": users[3].id,
                "tag_names": ["Testing", "Documentation"]
            },
        ]
        
        for proj_data in projects_data:
            tag_names = proj_data.pop("tag_names", [])
            
            project = Project(**proj_data)
            session.add(project)
            session.commit()
            session.refresh(project)
            
            # Link tags
            for tag_name in tag_names:
                tag = next((t for t in tags if t.name == tag_name), None)
                if tag:
                    link = ProjectTagLink(project_id=project.id, tag_id=tag.id)
                    session.add(link)
            
            session.commit()
        
        print(f"✅ Created {len(projects_data)} projects with tag associations")
        
        print("\n🎉 Data seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   Users: {len(users)}")
        print(f"   Tags: {len(tags)}")
        print(f"   Projects: {len(projects_data)}")
        print("\n🔐 Login Credentials:")
        print("   admin@example.com / admin123")
        print("   john@example.com / password123")
        print("   jane@example.com / password123")


if __name__ == "__main__":
    seed_data()
