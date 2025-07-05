#!/usr/bin/env python3
"""
TalentTrek - Job Market Analysis Platform
Main entry point for database initialization.
"""

import sys
from src.data.database import init_db
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Initialize the database."""
    logger.info("Initializing TalentTrek database...")
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
