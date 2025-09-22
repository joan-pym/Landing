import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import logging

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

class OAuthService:
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8001/auth/google/callback')
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.credentials_file = ROOT_DIR / 'oauth_credentials.json'
        
    def get_authorization_url(self):
        """Get the authorization URL for OAuth flow"""
        try:
            client_config = {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            return authorization_url, state
            
        except Exception as e:
            logger.error(f"Error getting authorization URL: {str(e)}")
            raise
    
    def exchange_code_for_credentials(self, authorization_code, state):
        """Exchange authorization code for credentials"""
        try:
            client_config = {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=self.scopes,
                state=state
            )
            flow.redirect_uri = self.redirect_uri
            
            flow.fetch_token(code=authorization_code)
            
            credentials = flow.credentials
            
            # Save credentials to file
            self.save_credentials(credentials)
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error exchanging code: {str(e)}")
            raise
    
    def save_credentials(self, credentials):
        """Save credentials to file"""
        try:
            creds_data = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            with open(self.credentials_file, 'w') as f:
                json.dump(creds_data, f)
                
            logger.info("Credentials saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving credentials: {str(e)}")
            raise
    
    def load_credentials(self):
        """Load credentials from file"""
        try:
            if not self.credentials_file.exists():
                return None
                
            with open(self.credentials_file, 'r') as f:
                creds_data = json.load(f)
            
            credentials = Credentials(
                token=creds_data['token'],
                refresh_token=creds_data.get('refresh_token'),
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )
            
            # Refresh token if expired
            if credentials.expired:
                credentials.refresh(Request())
                self.save_credentials(credentials)
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            return None
    
    def is_authenticated(self):
        """Check if we have valid credentials"""
        credentials = self.load_credentials()
        return credentials is not None and not credentials.expired
    
    def get_service(self, service_name, version):
        """Get authenticated Google API service"""
        credentials = self.load_credentials()
        if not credentials:
            raise Exception("Not authenticated. Need to complete OAuth flow first.")
            
        return build(service_name, version, credentials=credentials)