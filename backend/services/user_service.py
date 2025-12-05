from sqlmodel import Session, select
from models.user import User, UserCreate, UserUpdate
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuditService:
    """Simple audit logging service"""
    @staticmethod
    def log(action: str, entity_id: int, details: Optional[str] = None):
        print(f"[AUDIT] {datetime.utcnow()} - {action} - Entity: {entity_id} - {details}")


class UserService:
    """Business logic for User model"""
    
    @staticmethod
    def validate_user(data: UserCreate, session: Session) -> None:
        """Validation rules for user creation"""
        if len(data.full_name) < 3:
            raise ValueError("Full name must be at least 3 characters")
        
        if len(data.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Check email uniqueness
        existing = session.exec(select(User).where(User.email == data.email)).first()
        if existing:
            raise ValueError("Email already registered")
        
        # Validate role
        valid_roles = ["admin", "user", "viewer"]
        if data.role not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
    
    @staticmethod
    def validate_update(user_id: int, data: UserUpdate, session: Session) -> None:
        """Validation rules for user update"""
        if data.email:
            existing = session.exec(
                select(User).where(User.email == data.email, User.id != user_id)
            ).first()
            if existing:
                raise ValueError("Email already in use by another user")
        
        if data.role:
            valid_roles = ["admin", "user", "viewer"]
            if data.role not in valid_roles:
                raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def before_create(data: UserCreate, session: Session) -> dict:
        """Hook: before creating user"""
        UserService.validate_user(data, session)
        return {
            **data.model_dump(exclude={"password"}),
            "hashed_password": UserService.hash_password(data.password)
        }
    
    @staticmethod
    def after_create(user: User, session: Session):
        """Hook: after creating user"""
        AuditService.log("user_created", user.id, f"Email: {user.email}")
    
    @staticmethod
    def before_update(user_id: int, data: UserUpdate, session: Session) -> dict:
        """Hook: before updating user"""
        UserService.validate_update(user_id, data, session)
        update_data = data.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = UserService.hash_password(update_data.pop("password"))
        
        update_data["updated_at"] = datetime.utcnow()
        return update_data
    
    @staticmethod
    def after_update(user: User, session: Session):
        """Hook: after updating user"""
        AuditService.log("user_updated", user.id, f"Email: {user.email}")
    
    @staticmethod
    def before_delete(user: User, session: Session):
        """Hook: before deleting user"""
        # Check if user has projects
        if user.projects:
            raise ValueError(f"Cannot delete user with {len(user.projects)} projects. Reassign them first.")
    
    @staticmethod
    def after_delete(user_id: int, session: Session):
        """Hook: after deleting user"""
        AuditService.log("user_deleted", user_id)
    
    @staticmethod
    def enrich(user: User, session: Session) -> User:
        """Add computed fields"""
        user.project_count = len(user.projects) if user.projects else 0
        return user
