"""
Migration script to add new columns to existing tables
Run this inside the backend container
"""
import sys
sys.path.append('/app')

from sqlmodel import Session, create_engine, text
from core.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as session:
        try:
            # Add new columns to app table
            print("Adding new columns to app table...")
            
            # Add publish_status column with enum type
            session.exec(text("""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'publishstatus') THEN
                        CREATE TYPE publishstatus AS ENUM ('draft', 'published', 'unpublished');
                    END IF;
                END $$;
            """))
            
            session.exec(text("""
                ALTER TABLE app 
                ADD COLUMN IF NOT EXISTS publish_status publishstatus DEFAULT 'draft'
            """))
            
            # Add published_at column
            session.exec(text("""
                ALTER TABLE app 
                ADD COLUMN IF NOT EXISTS published_at TIMESTAMP
            """))
            
            # Add version column
            session.exec(text("""
                ALTER TABLE app 
                ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1
            """))
            
            session.commit()
            print("✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    migrate()
