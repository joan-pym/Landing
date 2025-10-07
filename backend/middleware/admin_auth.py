"""
Admin Authentication Middleware
Handles authentication independently of HTTPBasic to work around ingress issues
"""

import base64
import secrets
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os
import logging

logger = logging.getLogger(__name__)

class AdminAuthMiddleware(BaseHTTPMiddleware):
    """Custom middleware to handle admin authentication"""
    
    def __init__(self, app, admin_username: str = None, admin_password: str = None):
        super().__init__(app)
        self.admin_username = admin_username or os.getenv('ADMIN_USERNAME', 'pymetra_admin')
        self.admin_password = admin_password or os.getenv('ADMIN_PASSWORD', 'PymetraAdmin2024!Secure')
        
    async def dispatch(self, request: Request, call_next):
        # Only apply to admin routes
        if not request.url.path.startswith('/api/admin'):
            return await call_next(request)
        
        # Check for authentication header
        auth_header = request.headers.get('authorization', '')
        
        if not auth_header or not auth_header.startswith('Basic '):
            return self._authentication_required_response()
        
        try:
            # Decode credentials
            encoded_credentials = auth_header.split(' ', 1)[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Verify credentials
            is_correct_username = secrets.compare_digest(username, self.admin_username)
            is_correct_password = secrets.compare_digest(password, self.admin_password)
            
            if not (is_correct_username and is_correct_password):
                logger.warning(f"Invalid credentials attempt: {username}")
                return self._authentication_required_response()
            
            # Authentication successful
            logger.info(f"Admin authenticated: {username}")
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return self._authentication_required_response()
    
    def _authentication_required_response(self):
        """Return 401 with Basic Auth challenge"""
        return Response(
            status_code=401,
            content="Authentication required",
            headers={"WWW-Authenticate": "Basic realm=\"Pymetra Admin\""}
        )