import pytest
from unittest.mock import Mock, patch
from src.utils.supabase_auth import SupabaseAuth
from src.utils.supabase import SupabaseConfig

class TestSupabaseAuth:
    """Test Supabase authentication utilities."""
    
    @patch('src.utils.supabase_auth.supabase_config')
    def test_supabase_auth_initialization(self, mock_config):
        """Test Supabase Auth initialization."""
        mock_config.get_client.return_value = Mock()
        auth = SupabaseAuth()
        assert auth.client is not None
    
    @patch('src.utils.supabase_auth.supabase_config')
    def test_verify_token_with_valid_token(self, mock_config):
        """Test token verification with valid token."""
        mock_client = Mock()
        mock_user = Mock()
        mock_user.user.id = "test-user-id"
        mock_user.user.email = "test@example.com"
        mock_user.user.user_metadata = {"username": "testuser"}
        
        mock_client.auth.get_user.return_value = mock_user
        mock_config.get_client.return_value = mock_client
        
        auth = SupabaseAuth()
        result = auth.verify_token("valid.token.here")
        
        assert result is not None
        assert result["user_id"] == "test-user-id"
        assert result["email"] == "test@example.com"
        assert result["user_metadata"]["username"] == "testuser"
    
    @patch('src.utils.supabase_auth.supabase_config')
    def test_verify_token_with_invalid_token(self, mock_config):
        """Test token verification with invalid token."""
        mock_client = Mock()
        mock_client.auth.get_user.side_effect = Exception("Invalid token")
        mock_config.get_client.return_value = mock_client
        
        auth = SupabaseAuth()
        result = auth.verify_token("invalid.token.here")
        
        assert result is None
    
    @patch('src.utils.supabase_auth.supabase_config')
    def test_sign_up_success(self, mock_config):
        """Test successful user sign up."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.user = Mock()
        mock_response.session = Mock()
        mock_response.session.access_token = "test.access.token"
        
        mock_client.auth.sign_up.return_value = mock_response
        mock_config.get_client.return_value = mock_client
        
        auth = SupabaseAuth()
        result = auth.sign_up("test@example.com", "password123", {"username": "testuser"})
        
        assert result is not None
        assert "user" in result
        assert "session" in result
    
    @patch('src.utils.supabase_auth.supabase_config')
    def test_sign_in_success(self, mock_config):
        """Test successful user sign in."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.user = Mock()
        mock_response.session = Mock()
        mock_response.session.access_token = "test.access.token"
        
        mock_client.auth.sign_in_with_password.return_value = mock_response
        mock_config.get_client.return_value = mock_client
        
        auth = SupabaseAuth()
        result = auth.sign_in("test@example.com", "password123")
        
        assert result is not None
        assert "user" in result
        assert "session" in result

class TestSupabaseConfig:
    """Test Supabase configuration."""
    
    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test-service-key',
        'USE_SUPABASE_AUTH': 'true'
    })
    def test_supabase_config_with_auth_enabled(self):
        """Test Supabase config with auth enabled."""
        config = SupabaseConfig()
        assert config.url == 'https://test.supabase.co'
        assert config.anon_key == 'test-anon-key'
        assert config.service_role_key == 'test-service-key'
        assert config.use_supabase_auth is True
    
    @patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'USE_SUPABASE_AUTH': 'false'
    })
    def test_supabase_config_with_auth_disabled(self):
        """Test Supabase config with auth disabled."""
        config = SupabaseConfig()
        assert config.use_supabase_auth is False
    
    @patch.dict('os.environ', {})
    def test_supabase_config_without_credentials(self):
        """Test Supabase config without credentials."""
        config = SupabaseConfig()
        assert config.url is None
        assert config.anon_key is None
        assert config.use_supabase_auth is False 