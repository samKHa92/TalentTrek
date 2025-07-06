from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from src.supabase.supabase import supabase_config
from src.utils.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer()

class SupabaseAuth:
    """Supabase authentication utilities."""
    
    def __init__(self):
        self.client: Optional[Client] = supabase_config.get_client()
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a Supabase JWT token."""
        if not self.client:
            return None
        
        try:
            # Use Supabase client to verify the token
            user = self.client.auth.get_user(token)
            return {
                "user_id": user.user.id,
                "email": user.user.email,
                "user_metadata": user.user.user_metadata
            }
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """Get the current authenticated user from Supabase token."""
        if not self.client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Supabase client not configured"
            )
        
        try:
            user_data = self.verify_token(credentials.credentials)
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user_data
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def sign_up(self, email: str, password: str, user_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Sign up a new user with Supabase Auth."""
        if not self.client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Supabase client not configured"
            )
        
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_metadata or {}
                }
            })
            return {
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            logger.error(f"Sign up failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sign up failed: {str(e)}"
            )
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in a user with Supabase Auth."""
        if not self.client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Supabase client not configured"
            )
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    def sign_out(self, token: str) -> bool:
        """Sign out a user."""
        if not self.client:
            return False
        
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            logger.error(f"Sign out failed: {e}")
            return False

# Global Supabase Auth instance
supabase_auth = SupabaseAuth() 