from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Base
from src.utils.logger import get_logger
from src.utils.config import get_config
from src.utils.supabase import supabase_config

logger = get_logger(__name__)


def get_engine():
    """Get database engine, preferring Supabase PostgreSQL if configured."""
    # Use Supabase database URL if configured
    db_url = supabase_config.get_database_url()
    
    logger.info(f"Using database: {db_url}")
    
    # Configure engine based on database type
    if db_url.startswith('postgresql'):
        # PostgreSQL configuration
        engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20
        )
    else:
        # SQLite configuration (default)
        engine = create_engine(
            db_url, 
            echo=False, 
            connect_args={"check_same_thread": False}
        )
    
    return engine


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully.")
        
        # If using Supabase, log the connection status
        if supabase_config.is_configured():
            logger.info("Connected to Supabase PostgreSQL database")
        else:
            logger.info("Using local SQLite database")
            
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def get_session():
    """Get database session."""
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()
