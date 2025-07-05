import os
from supabase import create_client, Client
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SupabaseConfig:
    """Supabase configuration and client management."""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        # Default to false if Supabase is not configured
        self.use_supabase_auth = False
        if self.url and self.anon_key:
            self.use_supabase_auth = os.getenv("USE_SUPABASE_AUTH", "false").lower() == "true"
        
        self.client: Client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client."""
        if not self.url or not self.anon_key:
            logger.info("Supabase URL or anon key not provided. Supabase features will be disabled.")
            self.use_supabase_auth = False
            return
        
        try:
            # Use the basic create_client method
            self.client = create_client(self.url, self.anon_key)
            logger.info("Supabase client initialized successfully")
            if self.use_supabase_auth:
                logger.info("Supabase Auth is ENABLED - using Supabase authentication")
            else:
                logger.info("Supabase Auth is DISABLED - using local JWT authentication")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self.client = None
            self.use_supabase_auth = False
    
    def get_client(self) -> Client:
        """Get the Supabase client instance."""
        return self.client
    
    def is_configured(self) -> bool:
        """Check if Supabase is properly configured."""
        return self.client is not None and self.url and self.anon_key
    
    def use_supabase_auth_enabled(self) -> bool:
        """Check if Supabase Auth should be used instead of local auth."""
        return self.use_supabase_auth and self.is_configured()
    
    def get_database_url(self) -> str:
        """Get the database URL for SQLAlchemy."""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            logger.info("DATABASE_URL not provided, using default SQLite")
            return "sqlite:///data_output/jobs.db"
        return db_url

# Global Supabase configuration instance
supabase_config = SupabaseConfig() 