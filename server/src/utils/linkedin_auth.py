import os
import requests
import time
import webbrowser
import http.server
import socketserver
import threading
from urllib.parse import urlencode, urlparse, parse_qs
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LinkedInAuth:
    """LinkedIn OAuth authentication handler with automatic code capture."""
    
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_PRIMARY_CLIENT_SECRET")
        # Use host IP for Docker environments
        host_ip = os.getenv("HOST_IP", "localhost")
        self.redirect_uri = os.getenv("LINKEDIN_CALLBACK_REDIRECT_URL", f"http://{host_ip}:5173/callback")
        self.access_token = None
        self.token_expires_at = 0
        
        if not self.client_id or not self.client_secret:
            logger.warning("LinkedIn credentials not configured. Set LINKEDIN_CLIENT_ID and LINKEDIN_PRIMARY_CLIENT_SECRET environment variables.")
    
    def get_access_token(self):
        """Get a valid access token, refreshing if necessary."""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        return self._generate_access_token()
    
    def _generate_access_token(self):
        """Get access token from env var or start OAuth flow."""
        manual_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        if manual_token:
            self.access_token = manual_token
            self.token_expires_at = time.time() + (30 * 24 * 60 * 60)  # assume 30 days
            logger.info("Using LinkedIn access token from environment variable")
            return manual_token
        else:
            logger.info("No LinkedIn access token found. Starting OAuth flow...")
            return self.generate_token()
    
    def generate_token(self):
        """Run OAuth flow automatically with local callback server."""
        if not self.client_id or not self.client_secret:
            logger.error("LinkedIn credentials not configured")
            return None
        
        auth_url = self._get_authorization_url()
        logger.info(f"Opening browser to LinkedIn OAuth URL: {auth_url}")
        webbrowser.open(auth_url)  # automatically open the browser
        
        def start_callback_server(linkedin_auth):
            class OAuthHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    if "/callback" in self.path:
                        query = urlparse(self.path).query
                        params = parse_qs(query)
                        auth_code = params.get('code', [None])[0]
                        if auth_code:
                            logger.info("Authorization code received, exchanging for access token...")
                            linkedin_auth._exchange_code_for_token(auth_code)
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(b"<h1>LinkedIn authorization successful. You can close this window.</h1>")
                        else:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b"<h1>Error: Authorization code not found.</h1>")
            
            PORT = int(urlparse(self.redirect_uri).port or 80)
            with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
                logger.info(f"Listening on {self.redirect_uri} for LinkedIn OAuth callback...")
                httpd.serve_forever()
        
        # Start server in a separate thread so main thread can wait
        thread = threading.Thread(target=start_callback_server, args=(self,))
        thread.daemon = True
        thread.start()
        
        # Wait up to 5 minutes for token to be received
        start_time = time.time()
        while not self.access_token and time.time() - start_time < 300:
            time.sleep(1)
        
        if self.access_token:
            logger.info("LinkedIn access token obtained successfully")
        else:
            logger.error("Timed out waiting for LinkedIn authorization. Please try again.")
            logger.error("")
            logger.error("DOCKER USERS: If OAuth fails:")
            logger.error("- Set HOST_IP environment variable to your host machine IP")
            logger.error("- Or run 'make linkedin-auth-host' to use host networking")
            logger.error("- Or run 'make linkedin-auth-local' to run outside Docker")
        
        return self.access_token
    
    def _get_authorization_url(self):
        """Generate LinkedIn OAuth authorization URL."""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'r_liteprofile r_emailaddress w_member_social',
            'state': 'linkedin_oauth'
        }
        return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    
    def _exchange_code_for_token(self, auth_code):
        """Exchange authorization code for access token."""
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in', 3600)
            
            if access_token:
                self.access_token = access_token
                self.token_expires_at = time.time() + expires_in
                logger.info(f"LinkedIn access token generated successfully (expires in {expires_in} seconds)")
                return access_token
            else:
                logger.error("No access token in LinkedIn response")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to exchange authorization code for token: {e}")
            return None
    
    def get_auth_headers(self):
        """Get auth headers for LinkedIn API calls."""
        token = self.get_access_token()
        if token:
            return {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        return {}

# Global LinkedIn auth instance
linkedin_auth = LinkedInAuth()
