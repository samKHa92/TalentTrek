#!/usr/bin/env python3
"""
Initialize the TalentTrek database with Supabase PostgreSQL and authentication tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.database import init_db, get_session
from src.data.models import User, UserReport
from src.utils.logger import get_logger
from src.utils.supabase import supabase_config

logger = get_logger(__name__)

def create_sample_user():
    """Create a sample user for testing."""
    session = get_session()
    
    # Check if sample user already exists
    existing_user = session.query(User).filter(User.email == "admin@talenttrek.com").first()
    if existing_user:
        logger.info("Sample user already exists")
        return
    
    # Create sample user (for Supabase auth, we use a placeholder password)
    sample_user = User(
        email="admin@talenttrek.com",
        username="admin",
        hashed_password="supabase_auth",  # Placeholder since we're using Supabase Auth
        is_active=True
    )
    
    try:
        session.add(sample_user)
        session.commit()
        logger.info("Sample user created successfully")
        logger.info("Email: admin@talenttrek.com")
        logger.info("Note: This user needs to be created in Supabase Auth first")
    except Exception as e:
        logger.error(f"Failed to create sample user: {e}")
        session.rollback()
    finally:
        session.close()

def check_supabase_connection():
    """Check if Supabase is properly configured and accessible."""
    if not supabase_config.is_configured():
        logger.warning("Supabase is not configured. Check your environment variables.")
        return False
    
    try:
        # Test database connection
        from sqlalchemy import text
        session = get_session()
        session.execute(text("SELECT 1"))
        session.close()
        logger.info("Supabase PostgreSQL connection successful!")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Supabase PostgreSQL: {e}")
        logger.error("Please check your DATABASE_URL and Supabase configuration.")
        return False

def main():
    """Initialize the Supabase database and create sample data."""
    logger.info("Initializing TalentTrek database with Supabase PostgreSQL...")
    
    # Check Supabase configuration
    if not check_supabase_connection():
        logger.error("Cannot proceed without proper Supabase configuration.")
        sys.exit(1)
    
    try:
        # Initialize database tables
        init_db()
        logger.info("Database tables created successfully in Supabase PostgreSQL")
        
        # Create sample user
        create_sample_user()
        
        logger.info("Supabase database initialization completed successfully!")
        logger.info("You can now start the application and register/login with Supabase Auth")
        
        # Log Supabase configuration status
        if supabase_config.use_supabase_auth_enabled():
            logger.info("Supabase Auth is ENABLED - using Supabase authentication")
        else:
            logger.info("Supabase Auth is DISABLED - using local JWT authentication")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 