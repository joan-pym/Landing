#!/usr/bin/env python3
"""
Targeted Proxy Authentication Test
Tests if HTTPBasic authentication works through the proxy/ingress
"""

import requests
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URLs
EXTERNAL_URL = "https://pymetra.com"
LOCAL_URL = "http://localhost:8001"

# Admin credentials
ADMIN_USERNAME = "pymetra_admin"
ADMIN_PASSWORD = "PymetraAdmin2024!Secure"

def test_auth_headers():
    """Test different ways of sending authentication"""
    
    # Prepare auth
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    auth_methods = [
        ("Basic Auth Header", {'Authorization': f'Basic {encoded_credentials}'}),
        ("Requests Auth", None)  # Will use requests.auth.HTTPBasicAuth
    ]
    
    endpoints = [
        ("/api/admin/", "Admin Dashboard"),
        ("/api/admin/export/csv", "CSV Export")
    ]
    
    for endpoint, endpoint_name in endpoints:
        logger.info(f"\n=== Testing {endpoint_name} ({endpoint}) ===")
        
        for auth_name, headers in auth_methods:
            logger.info(f"\n--- {auth_name} ---")
            
            # Test locally
            try:
                if headers:
                    local_response = requests.get(f"{LOCAL_URL}{endpoint}", headers=headers, timeout=10)
                else:
                    local_response = requests.get(f"{LOCAL_URL}{endpoint}", 
                                                auth=(ADMIN_USERNAME, ADMIN_PASSWORD), timeout=10)
                logger.info(f"Local: {local_response.status_code}")
            except Exception as e:
                logger.error(f"Local error: {e}")
            
            # Test externally
            try:
                if headers:
                    external_response = requests.get(f"{EXTERNAL_URL}{endpoint}", headers=headers, timeout=30)
                else:
                    external_response = requests.get(f"{EXTERNAL_URL}{endpoint}", 
                                                   auth=(ADMIN_USERNAME, ADMIN_PASSWORD), timeout=30)
                logger.info(f"External: {external_response.status_code}")
                
                # Check response content for admin panel
                if endpoint == "/api/admin/" and external_response.status_code == 200:
                    content = external_response.text.lower()
                    has_admin = 'admin' in content and 'pymetra' in content
                    logger.info(f"External admin panel content valid: {has_admin}")
                    
            except Exception as e:
                logger.error(f"External error: {e}")

def test_without_auth():
    """Test endpoints without authentication"""
    logger.info(f"\n=== Testing WITHOUT Authentication ===")
    
    endpoints = [
        ("/api/admin/", "Admin Dashboard"),
        ("/api/admin/export/csv", "CSV Export")
    ]
    
    for endpoint, endpoint_name in endpoints:
        logger.info(f"\n--- {endpoint_name} ({endpoint}) ---")
        
        # Test locally
        try:
            local_response = requests.get(f"{LOCAL_URL}{endpoint}", timeout=10)
            logger.info(f"Local (no auth): {local_response.status_code}")
        except Exception as e:
            logger.error(f"Local error: {e}")
        
        # Test externally
        try:
            external_response = requests.get(f"{EXTERNAL_URL}{endpoint}", timeout=30)
            logger.info(f"External (no auth): {external_response.status_code}")
        except Exception as e:
            logger.error(f"External error: {e}")

if __name__ == "__main__":
    logger.info("=== PROXY AUTHENTICATION TEST ===")
    logger.info(f"Local URL: {LOCAL_URL}")
    logger.info(f"External URL: {EXTERNAL_URL}")
    logger.info(f"Admin credentials: {ADMIN_USERNAME}:{ADMIN_PASSWORD}")
    
    test_without_auth()
    test_auth_headers()
    
    logger.info("\n=== TEST COMPLETE ===")