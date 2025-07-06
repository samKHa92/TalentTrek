#!/usr/bin/env python3
"""
Seed script for creating sample data in TalentTrek database.
Run this after applying migrations if you need sample data for testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import get_session
from src.data.models import User
from src.utils.logger import get_logger

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

def main():
    """Create sample data."""
    logger.info("Creating sample data...")
    
    try:
        create_sample_user()
        logger.info("Sample data creation completed successfully!")
        
    except Exception as e:
        logger.error(f"Sample data creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 