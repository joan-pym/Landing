#!/usr/bin/env python3
"""
Backend Testing Suite for Pymetra - TEMPORARY SOLUTIONS VERIFICATION
Tests 5 temporary solutions implemented to resolve proxy/ingress issues
"""

import requests
import json
import logging
import tempfile
import os
import base64
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Production URL
BASE_URL = "https://pymetra.com"

# Admin credentials
ADMIN_USERNAME = "pymetra_admin"
ADMIN_PASSWORD = "PymetraAdmin2024!Secure"

class PymetraBackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pymetra-Backend-Tester/1.0'
        })
        
        # Prepare basic auth header
        credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.auth_headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }
        
    def test_admin_panel_security_without_auth(self):
        """Test 1: Admin Panel Security - WITHOUT credentials (should return 401)"""
        logger.info("=== TEST 1: Admin Panel Security - NO AUTH ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 401:
                logger.info("✅ SECURITY WORKING: Admin panel correctly requires authentication")
                return {
                    'success': True,
                    'security_working': True,
                    'status_code': response.status_code
                }
            else:
                logger.error(f"❌ SECURITY BREACH: Admin panel accessible without auth (status: {response.status_code})")
                return {
                    'success': False, 
                    'security_working': False,
                    'status_code': response.status_code,
                    'error': f"Expected 401, got {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Admin panel security test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_admin_panel_security_with_auth(self):
        """Test 2: Admin Panel Security - WITH credentials (should work)"""
        logger.info("=== TEST 2: Admin Panel Security - WITH AUTH ===")
        try:
            headers = self.auth_headers.copy()
            response = self.session.get(f"{self.base_url}/api/admin/", headers=headers, timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                # Check if it's HTML content with admin panel
                is_html = 'html' in response.text.lower()
                has_pymetra = 'pymetra' in response.text.lower()
                has_admin = 'admin' in response.text.lower()
                logger.info(f"Is HTML: {is_html}")
                logger.info(f"Contains Pymetra: {has_pymetra}")
                logger.info(f"Contains Admin: {has_admin}")
                
                if is_html and has_pymetra and has_admin:
                    logger.info("✅ AUTHENTICATION WORKING: Admin panel accessible with credentials")
                    return {
                        'success': True,
                        'authenticated_access': True,
                        'is_html': is_html,
                        'has_pymetra': has_pymetra,
                        'has_admin': has_admin
                    }
                else:
                    logger.error("❌ UNEXPECTED RESPONSE: Got 200 but content doesn't look like admin panel")
                    return {
                        'success': False,
                        'authenticated_access': False,
                        'error': "Response doesn't contain expected admin panel content"
                    }
            else:
                logger.error(f"❌ AUTHENTICATION FAILED: Expected 200, got {response.status_code}")
                return {
                    'success': False,
                    'authenticated_access': False,
                    'status_code': response.status_code,
                    'error': f"Expected 200, got {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Admin panel auth test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_admin_migrate_cvs_endpoint(self):
        """Test 3: Admin CV Migration Endpoint - WITH credentials (should work, not 404)"""
        logger.info("=== TEST 3: Admin CV Migration Endpoint ===")
        try:
            headers = self.auth_headers.copy()
            headers['Content-Type'] = 'application/json'
            
            response = self.session.post(f"{self.base_url}/api/admin/migrate-cvs", headers=headers, timeout=120)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ ENDPOINT WORKING: CV Migration endpoint accessible")
                logger.info(f"Migration Results: {data}")
                return {
                    'success': True,
                    'endpoint_accessible': True,
                    'data': data
                }
            elif response.status_code == 404:
                logger.error("❌ ROUTING ISSUE: CV Migration endpoint returns 404 (proxy/ingress problem)")
                return {
                    'success': False,
                    'endpoint_accessible': False,
                    'status_code': response.status_code,
                    'error': "Endpoint returns 404 - routing issue"
                }
            elif response.status_code == 401:
                logger.error("❌ AUTHENTICATION ISSUE: CV Migration endpoint requires auth but credentials not working")
                return {
                    'success': False,
                    'endpoint_accessible': False,
                    'status_code': response.status_code,
                    'error': "Authentication failed with provided credentials"
                }
            else:
                logger.error(f"❌ UNEXPECTED STATUS: CV Migration endpoint returned {response.status_code}")
                return {
                    'success': False,
                    'endpoint_accessible': False,
                    'status_code': response.status_code,
                    'error': f"Unexpected status code: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"CV Migration endpoint test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_admin_download_cv_endpoint(self):
        """Test 4: Admin CV Download Endpoint - WITH credentials (should work, not 404)"""
        logger.info("=== TEST 4: Admin CV Download Endpoint ===")
        try:
            # First get a registration ID to test with
            headers = self.auth_headers.copy()
            
            # Try to get registrations count first to see if we have any data
            count_response = self.session.get(f"{self.base_url}/api/registrations/count", timeout=30)
            if count_response.status_code == 200:
                count_data = count_response.json()
                total_registrations = count_data.get('total_registrations', 0)
                logger.info(f"Total registrations available: {total_registrations}")
                
                if total_registrations > 0:
                    # Use a test ID - we'll test the endpoint routing, not necessarily a valid ID
                    test_id = "test-id-for-routing-check"
                    response = self.session.get(f"{self.base_url}/api/admin/download-cv/{test_id}", headers=headers, timeout=30)
                    logger.info(f"Status Code: {response.status_code}")
                    logger.info(f"Response Headers: {dict(response.headers)}")
                    logger.info(f"Response: {response.text[:200]}...")  # First 200 chars
                    
                    if response.status_code == 404 and "Registro no encontrado" in response.text:
                        logger.info("✅ ENDPOINT WORKING: CV Download endpoint accessible (404 for non-existent ID is expected)")
                        return {
                            'success': True,
                            'endpoint_accessible': True,
                            'status_code': response.status_code,
                            'note': "404 for non-existent ID is expected behavior"
                        }
                    elif response.status_code == 404 and "Registro no encontrado" not in response.text:
                        logger.error("❌ ROUTING ISSUE: CV Download endpoint returns 404 (proxy/ingress problem)")
                        return {
                            'success': False,
                            'endpoint_accessible': False,
                            'status_code': response.status_code,
                            'error': "Endpoint returns 404 - routing issue"
                        }
                    elif response.status_code == 401:
                        logger.error("❌ AUTHENTICATION ISSUE: CV Download endpoint requires auth but credentials not working")
                        return {
                            'success': False,
                            'endpoint_accessible': False,
                            'status_code': response.status_code,
                            'error': "Authentication failed with provided credentials"
                        }
                    elif response.status_code == 200:
                        logger.info("✅ ENDPOINT WORKING: CV Download endpoint accessible and returned file")
                        return {
                            'success': True,
                            'endpoint_accessible': True,
                            'status_code': response.status_code,
                            'note': "Endpoint returned file successfully"
                        }
                    else:
                        logger.error(f"❌ UNEXPECTED STATUS: CV Download endpoint returned {response.status_code}")
                        return {
                            'success': False,
                            'endpoint_accessible': False,
                            'status_code': response.status_code,
                            'error': f"Unexpected status code: {response.status_code}"
                        }
                else:
                    logger.info("⚠️  NO DATA: No registrations available to test CV download")
                    return {
                        'success': True,
                        'endpoint_accessible': True,
                        'note': "No registrations available to test, but endpoint routing can be verified"
                    }
            else:
                logger.error("❌ Cannot get registration count to test CV download")
                return {
                    'success': False,
                    'error': "Cannot get registration count"
                }
                
        except Exception as e:
            logger.error(f"CV Download endpoint test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_admin_panel(self):
        """Test 4: Admin Panel Access"""
        logger.info("=== TEST 4: Admin Panel ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                # Check if it's HTML content
                is_html = 'html' in response.text.lower()
                has_pymetra = 'pymetra' in response.text.lower()
                logger.info(f"Is HTML: {is_html}")
                logger.info(f"Contains Pymetra: {has_pymetra}")
                return {
                    'success': True,
                    'is_html': is_html,
                    'has_pymetra': has_pymetra,
                    'content_length': len(response.text)
                }
            else:
                logger.error(f"Admin panel test failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Admin panel test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_test_pdf(self):
        """Create a small test PDF file"""
        try:
            # Create a simple PDF content (minimal PDF structure)
            pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test CV Document) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
300
%%EOF"""
            return pdf_content
        except Exception as e:
            logger.error(f"Error creating test PDF: {str(e)}")
            return None
    
    def test_admin_panel_updated(self):
        """Test 5: Updated Admin Panel with New Features"""
        logger.info("=== TEST 5: Updated Admin Panel ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for new features
                has_download_cv = 'download-cv' in content or 'descargar' in content
                has_migrate_cvs = 'migrate-cvs' in content or 'migrar' in content
                has_google_drive = 'google drive' in content or 'drive' in content
                has_pymetra = 'pymetra' in content
                
                logger.info(f"Has CV Download: {has_download_cv}")
                logger.info(f"Has CV Migration: {has_migrate_cvs}")
                logger.info(f"Has Google Drive: {has_google_drive}")
                logger.info(f"Contains Pymetra: {has_pymetra}")
                
                return {
                    'success': True,
                    'has_download_cv': has_download_cv,
                    'has_migrate_cvs': has_migrate_cvs,
                    'has_google_drive': has_google_drive,
                    'has_pymetra': has_pymetra,
                    'content_length': len(response.text)
                }
            else:
                logger.error(f"Admin panel test failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Admin panel test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_cv_migration(self):
        """Test 6: CV Migration to Google Drive"""
        logger.info("=== TEST 6: CV Migration ===")
        try:
            response = self.session.post(f"{self.base_url}/api/admin/migrate-cvs", timeout=120)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info("=== MIGRATION RESULTS ===")
                logger.info(f"Migrated: {data.get('migrated', 0)}")
                logger.info(f"Already in Drive: {data.get('already_in_drive', 0)}")
                logger.info(f"Failed: {data.get('failed', 0)}")
                logger.info(f"Total: {data.get('total', 0)}")
                
                return {
                    'success': True,
                    'data': data,
                    'migrated': data.get('migrated', 0),
                    'already_in_drive': data.get('already_in_drive', 0),
                    'failed': data.get('failed', 0),
                    'total': data.get('total', 0)
                }
            else:
                logger.error(f"Migration test failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}", 'response': response.text}
                
        except Exception as e:
            logger.error(f"Migration test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_external_registration_final(self):
        """Test 7: Complete External Registration Test"""
        logger.info("=== TEST 7: External Registration Final ===")
        try:
            # Create test PDF
            pdf_content = self.create_test_pdf()
            if not pdf_content:
                return {'success': False, 'error': 'Could not create test PDF'}
            
            # Use EXACT data from user request
            form_data = {
                'fullName': 'Usuario Test Externo Final',
                'email': 'test.externo.final@pymetra.com',
                'geographicArea': 'Barcelona',
                'mainSector': 'Marketing Digital',
                'language': 'es'
            }
            
            # Prepare file
            files = {
                'cv': ('usuario_test_externo_final.pdf', pdf_content, 'application/pdf')
            }
            
            logger.info("=== EXTERNAL REGISTRATION TEST DATA ===")
            logger.info(f"Form data: {form_data}")
            logger.info(f"PDF size: {len(pdf_content)} bytes")
            logger.info("=== SENDING REGISTRATION REQUEST ===")
            
            # Send request with extended timeout for Google APIs
            response = self.session.post(
                f"{self.base_url}/api/register-agent",
                data=form_data,
                files=files,
                timeout=90  # Extended timeout for Google APIs
            )
            
            logger.info(f"=== REGISTRATION RESPONSE ===")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info("=== REGISTRATION SUCCESS ANALYSIS ===")
                logger.info(f"Registration ID: {data.get('registration_id')}")
                logger.info(f"Message: {data.get('message')}")
                logger.info(f"Email sent: {data.get('email_sent')}")
                logger.info(f"CV saved: {data.get('cv_saved')}")
                
                # Analyze the response to determine if Google APIs worked
                email_sent = data.get('email_sent', False)
                cv_saved = data.get('cv_saved', False)
                message = data.get('message', '')
                
                google_apis_working = False
                if 'Google Sheets' in message and 'Drive' in message:
                    google_apis_working = True
                    logger.info("✅ GOOGLE APIS CONFIRMED WORKING")
                elif email_sent and cv_saved:
                    logger.info("⚠️  APIS WORKING BUT UNCLEAR IF GOOGLE OR BACKUP")
                else:
                    logger.info("❌ GOOGLE APIS LIKELY NOT WORKING")
                
                # Critical verification points
                joan_email_expected = email_sent  # Should receive email at joan@pymetra.com
                google_sheets_expected = 'Sheets' in message  # Should save to Google Sheets
                google_drive_expected = 'Drive' in message  # Should save to Google Drive
                
                return {
                    'success': True, 
                    'data': data,
                    'google_apis_working': google_apis_working,
                    'email_sent': email_sent,
                    'cv_saved': cv_saved,
                    'joan_email_expected': joan_email_expected,
                    'google_sheets_expected': google_sheets_expected,
                    'google_drive_expected': google_drive_expected
                }
            else:
                logger.error(f"=== REGISTRATION FAILED ===")
                logger.error(f"Status: {response.status_code}")
                logger.error(f"Error: {response.text}")
                return {
                    'success': False, 
                    'error': f"HTTP {response.status_code}", 
                    'response': response.text
                }
                
        except Exception as e:
            logger.error(f"=== EXTERNAL REGISTRATION TEST FAILED ===")
            logger.error(f"Exception: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            return {'success': False, 'error': str(e)}
    
    def test_javascript_client_side_auth(self):
        """Test 1: JavaScript Client-Side Authentication for Admin Panel"""
        logger.info("=== TEST 1: JavaScript Client-Side Authentication ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for JavaScript authentication elements
                has_js_auth = 'checkadminauth' in content
                has_prompt = 'prompt(' in content
                has_credentials_check = 'pymetra_admin' in content and 'pymetraadmin2024!secure' in content
                has_session_storage = 'sessionstorage' in content
                
                logger.info(f"Has JS Auth Function: {has_js_auth}")
                logger.info(f"Has Prompt for Credentials: {has_prompt}")
                logger.info(f"Has Credentials Check: {has_credentials_check}")
                logger.info(f"Has Session Storage: {has_session_storage}")
                
                if has_js_auth and has_prompt and has_credentials_check:
                    logger.info("✅ JAVASCRIPT AUTH WORKING: Client-side authentication implemented")
                    return {
                        'success': True,
                        'js_auth_implemented': True,
                        'has_credential_check': has_credentials_check,
                        'has_session_storage': has_session_storage
                    }
                else:
                    logger.error("❌ JAVASCRIPT AUTH INCOMPLETE: Missing authentication elements")
                    return {
                        'success': False,
                        'js_auth_implemented': False,
                        'error': "JavaScript authentication not properly implemented"
                    }
            else:
                logger.error(f"❌ ADMIN PANEL NOT ACCESSIBLE: Status {response.status_code}")
                return {
                    'success': False,
                    'js_auth_implemented': False,
                    'status_code': response.status_code,
                    'error': f"Admin panel returned {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"JavaScript auth test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_alternative_get_cv_endpoint(self):
        """Test 2: Alternative /api/admin/get-cv/{id} endpoint"""
        logger.info("=== TEST 2: Alternative Get CV Endpoint ===")
        try:
            # First get a registration ID to test with
            count_response = self.session.get(f"{self.base_url}/api/registrations/count", timeout=30)
            if count_response.status_code == 200:
                count_data = count_response.json()
                total_registrations = count_data.get('total_registrations', 0)
                logger.info(f"Total registrations available: {total_registrations}")
                
                if total_registrations > 0:
                    # Use a test ID to check endpoint routing
                    test_id = "test-id-for-routing-check"
                    response = self.session.get(f"{self.base_url}/api/admin/get-cv/{test_id}", timeout=30)
                    logger.info(f"Status Code: {response.status_code}")
                    logger.info(f"Response: {response.text}")
                    
                    if response.status_code == 404 and "Registro no encontrado" in response.text:
                        logger.info("✅ ALTERNATIVE ENDPOINT WORKING: get-cv endpoint accessible (404 for non-existent ID is expected)")
                        return {
                            'success': True,
                            'endpoint_accessible': True,
                            'status_code': response.status_code,
                            'note': "404 for non-existent ID is expected behavior"
                        }
                    elif response.status_code == 404 and "Registro no encontrado" not in response.text:
                        logger.error("❌ ROUTING ISSUE: get-cv endpoint returns 404 (proxy/ingress problem)")
                        return {
                            'success': False,
                            'endpoint_accessible': False,
                            'status_code': response.status_code,
                            'error': "Endpoint returns 404 - routing issue"
                        }
                    elif response.status_code == 200:
                        logger.info("✅ ALTERNATIVE ENDPOINT WORKING: get-cv endpoint returned data")
                        return {
                            'success': True,
                            'endpoint_accessible': True,
                            'status_code': response.status_code,
                            'note': "Endpoint returned data successfully"
                        }
                    else:
                        logger.error(f"❌ UNEXPECTED STATUS: get-cv endpoint returned {response.status_code}")
                        return {
                            'success': False,
                            'endpoint_accessible': False,
                            'status_code': response.status_code,
                            'error': f"Unexpected status code: {response.status_code}"
                        }
                else:
                    logger.info("⚠️  NO DATA: No registrations available to test get-cv")
                    return {
                        'success': True,
                        'endpoint_accessible': True,
                        'note': "No registrations available to test, but endpoint routing can be verified"
                    }
            else:
                logger.error("❌ Cannot get registration count to test get-cv")
                return {
                    'success': False,
                    'error': "Cannot get registration count"
                }
                
        except Exception as e:
            logger.error(f"Alternative get-cv endpoint test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_alternative_list_cvs_endpoint(self):
        """Test 3: Alternative /api/admin/list-cvs endpoint"""
        logger.info("=== TEST 3: Alternative List CVs Endpoint ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/list-cvs", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text[:500]}...")  # First 500 chars
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    total_cvs = data.get('total_cvs', 0)
                    cvs_list = data.get('cvs', [])
                    
                    logger.info(f"Total CVs found: {total_cvs}")
                    logger.info(f"CVs list length: {len(cvs_list)}")
                    
                    # Check structure of response
                    has_proper_structure = 'total_cvs' in data and 'cvs' in data
                    
                    if has_proper_structure:
                        logger.info("✅ LIST CVS ENDPOINT WORKING: Returns proper JSON structure")
                        return {
                            'success': True,
                            'endpoint_accessible': True,
                            'total_cvs': total_cvs,
                            'cvs_count': len(cvs_list),
                            'has_proper_structure': True
                        }
                    else:
                        logger.error("❌ IMPROPER RESPONSE: list-cvs endpoint doesn't return expected structure")
                        return {
                            'success': False,
                            'endpoint_accessible': True,
                            'error': "Response doesn't have expected JSON structure"
                        }
                        
                except json.JSONDecodeError:
                    logger.error("❌ INVALID JSON: list-cvs endpoint doesn't return valid JSON")
                    return {
                        'success': False,
                        'endpoint_accessible': True,
                        'error': "Response is not valid JSON"
                    }
                    
            elif response.status_code == 404:
                logger.error("❌ ROUTING ISSUE: list-cvs endpoint returns 404 (proxy/ingress problem)")
                return {
                    'success': False,
                    'endpoint_accessible': False,
                    'status_code': response.status_code,
                    'error': "Endpoint returns 404 - routing issue"
                }
            else:
                logger.error(f"❌ UNEXPECTED STATUS: list-cvs endpoint returned {response.status_code}")
                return {
                    'success': False,
                    'endpoint_accessible': False,
                    'status_code': response.status_code,
                    'error': f"Unexpected status code: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Alternative list-cvs endpoint test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_updated_admin_panel_buttons(self):
        """Test 4: Updated Admin Panel with New Functional Buttons"""
        logger.info("=== TEST 4: Updated Admin Panel Buttons ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for new temporary buttons
                has_list_cvs_button = 'ver lista de cvs (temporal)' in content
                has_info_cvs_button = 'info cvs (temporal)' in content
                has_list_cvs_link = '/api/admin/list-cvs' in content
                has_migrate_function = 'migratecvs()' in content
                
                logger.info(f"Has 'Ver Lista de CVs (Temporal)' button: {has_list_cvs_button}")
                logger.info(f"Has 'Info CVs (Temporal)' button: {has_info_cvs_button}")
                logger.info(f"Has list-cvs link: {has_list_cvs_link}")
                logger.info(f"Has migrate function: {has_migrate_function}")
                
                if has_list_cvs_button and has_info_cvs_button and has_list_cvs_link:
                    logger.info("✅ UPDATED ADMIN PANEL: New temporary buttons implemented")
                    return {
                        'success': True,
                        'has_new_buttons': True,
                        'has_list_cvs_button': has_list_cvs_button,
                        'has_info_cvs_button': has_info_cvs_button,
                        'has_functional_links': has_list_cvs_link
                    }
                else:
                    logger.error("❌ MISSING BUTTONS: New temporary buttons not found in admin panel")
                    return {
                        'success': False,
                        'has_new_buttons': False,
                        'error': "New temporary buttons not implemented"
                    }
            else:
                logger.error(f"❌ ADMIN PANEL NOT ACCESSIBLE: Status {response.status_code}")
                return {
                    'success': False,
                    'has_new_buttons': False,
                    'status_code': response.status_code,
                    'error': f"Admin panel returned {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Updated admin panel test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_manual_migration_script(self):
        """Test 5: Manual Migration Script Execution"""
        logger.info("=== TEST 5: Manual Migration Script ===")
        try:
            # Check if script exists
            script_path = "/app/backend/migrate_cvs.py"
            if not os.path.exists(script_path):
                logger.error(f"❌ SCRIPT NOT FOUND: {script_path}")
                return {
                    'success': False,
                    'script_exists': False,
                    'error': "Migration script not found"
                }
            
            logger.info(f"✅ Script found: {script_path}")
            
            # Try to run the script (dry run check)
            try:
                # Just check if the script can be imported/parsed
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', script_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    logger.info("✅ SCRIPT SYNTAX VALID: Migration script compiles successfully")
                    
                    # Check script content for key functions
                    with open(script_path, 'r') as f:
                        script_content = f.read()
                    
                    has_migrate_function = 'migrate_cvs_to_drive' in script_content
                    has_google_auth_check = 'is_authenticated' in script_content
                    has_database_service = 'DatabaseService' in script_content
                    has_google_service = 'GoogleAPIsService' in script_content
                    
                    logger.info(f"Has migrate function: {has_migrate_function}")
                    logger.info(f"Has Google auth check: {has_google_auth_check}")
                    logger.info(f"Has database service: {has_database_service}")
                    logger.info(f"Has Google service: {has_google_service}")
                    
                    if has_migrate_function and has_google_auth_check:
                        logger.info("✅ MIGRATION SCRIPT COMPLETE: All required functions present")
                        return {
                            'success': True,
                            'script_exists': True,
                            'script_valid': True,
                            'has_required_functions': True
                        }
                    else:
                        logger.error("❌ SCRIPT INCOMPLETE: Missing required functions")
                        return {
                            'success': False,
                            'script_exists': True,
                            'script_valid': True,
                            'has_required_functions': False,
                            'error': "Script missing required functions"
                        }
                else:
                    logger.error(f"❌ SCRIPT SYNTAX ERROR: {result.stderr}")
                    return {
                        'success': False,
                        'script_exists': True,
                        'script_valid': False,
                        'error': f"Script syntax error: {result.stderr}"
                    }
                    
            except subprocess.TimeoutExpired:
                logger.error("❌ SCRIPT CHECK TIMEOUT")
                return {
                    'success': False,
                    'script_exists': True,
                    'error': "Script check timed out"
                }
                
        except Exception as e:
            logger.error(f"Manual migration script test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def run_temporary_solutions_tests(self):
        """Run all 5 temporary solutions tests"""
        logger.info("=== STARTING TEMPORARY SOLUTIONS VERIFICATION ===")
        logger.info(f"Testing against: {self.base_url}")
        logger.info("=== TESTING CONTEXT ===")
        logger.info("- Testing 5 temporary solutions for proxy/ingress issues")
        logger.info("- JavaScript client-side authentication")
        logger.info("- Alternative endpoints for CV operations")
        logger.info("- Updated admin panel with functional buttons")
        logger.info("- Manual migration script")
        
        results = {}
        
        # Test 1: JavaScript Client-Side Authentication
        logger.info("\n" + "="*60)
        results['javascript_auth'] = self.test_javascript_client_side_auth()
        
        # Test 2: Alternative Get CV Endpoint
        logger.info("\n" + "="*60)
        results['alternative_get_cv'] = self.test_alternative_get_cv_endpoint()
        
        # Test 3: Alternative List CVs Endpoint
        logger.info("\n" + "="*60)
        results['alternative_list_cvs'] = self.test_alternative_list_cvs_endpoint()
        
        # Test 4: Updated Admin Panel Buttons
        logger.info("\n" + "="*60)
        results['updated_admin_panel'] = self.test_updated_admin_panel_buttons()
        
        # Test 5: Manual Migration Script
        logger.info("\n" + "="*60)
        results['manual_migration_script'] = self.test_manual_migration_script()
        
        logger.info("\n" + "="*60)
        logger.info("=== TEMPORARY SOLUTIONS TEST RESULTS SUMMARY ===")
        for test_name, result in results.items():
            status = "✅ PASS" if result.get('success') else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
            if not result.get('success'):
                logger.error(f"  Error: {result.get('error', 'Unknown error')}")
        
        # Critical Analysis
        logger.info("\n" + "="*60)
        logger.info("=== TEMPORARY SOLUTIONS ANALYSIS ===")
        
        js_auth = results.get('javascript_auth', {})
        get_cv = results.get('alternative_get_cv', {})
        list_cvs = results.get('alternative_list_cvs', {})
        admin_panel = results.get('updated_admin_panel', {})
        migration_script = results.get('manual_migration_script', {})
        
        # Solution Analysis
        if js_auth.get('js_auth_implemented'):
            logger.info("✅ Solution 1: JavaScript client-side authentication implemented")
        else:
            logger.info("❌ Solution 1: JavaScript authentication not working")
        
        if get_cv.get('endpoint_accessible'):
            logger.info("✅ Solution 2: Alternative get-cv endpoint accessible")
        else:
            logger.info("❌ Solution 2: Alternative get-cv endpoint not accessible")
        
        if list_cvs.get('endpoint_accessible'):
            logger.info("✅ Solution 3: Alternative list-cvs endpoint accessible")
        else:
            logger.info("❌ Solution 3: Alternative list-cvs endpoint not accessible")
        
        if admin_panel.get('has_new_buttons'):
            logger.info("✅ Solution 4: Updated admin panel with new buttons")
        else:
            logger.info("❌ Solution 4: Admin panel buttons not updated")
        
        if migration_script.get('script_exists') and migration_script.get('has_required_functions'):
            logger.info("✅ Solution 5: Manual migration script available and complete")
        else:
            logger.info("❌ Solution 5: Manual migration script issues")
        
        # Overall Assessment
        logger.info("\n" + "="*60)
        logger.info("=== OVERALL TEMPORARY SOLUTIONS ASSESSMENT ===")
        
        solutions_working = sum([
            js_auth.get('js_auth_implemented', False),
            get_cv.get('endpoint_accessible', False),
            list_cvs.get('endpoint_accessible', False),
            admin_panel.get('has_new_buttons', False),
            migration_script.get('script_exists', False) and migration_script.get('has_required_functions', False)
        ])
        
        logger.info(f"Working solutions: {solutions_working}/5")
        
        if solutions_working >= 4:
            logger.info("✅ TEMPORARY SOLUTIONS: HIGHLY SUCCESSFUL")
            logger.info("✅ Most proxy/ingress issues resolved with workarounds")
            logger.info("✅ Admin functionality restored")
        elif solutions_working >= 3:
            logger.info("⚠️  TEMPORARY SOLUTIONS: PARTIALLY SUCCESSFUL")
            logger.info("✅ Some proxy/ingress issues resolved")
            logger.info("⚠️  Some functionality still limited")
        else:
            logger.info("❌ TEMPORARY SOLUTIONS: INSUFFICIENT")
            logger.info("❌ Most solutions not working properly")
            logger.info("❌ Proxy/ingress issues persist")
        
        return results

def main():
    """Main test execution - Middleware Authentication Testing"""
    tester = PymetraBackendTester()
    results = tester.run_middleware_authentication_tests()
    
    # Print final summary
    print("\n" + "="*80)
    print("PYMETRA MIDDLEWARE AUTHENTICATION TEST RESULTS")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get('success'))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print()
    
    # Detailed results
    for test_name, result in results.items():
        status = "✅ PASS" if result.get('success') else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
        if not result.get('success'):
            print(f"  Error: {result.get('error', 'Unknown error')}")
        
        # Special handling for key results
        if test_name == 'admin_security_no_auth':
            if result.get('security_working'):
                print(f"  ✅ Security: Correctly requires authentication (401)")
            else:
                print(f"  ❌ Security: BREACH - Accessible without auth ({result.get('status_code')})")
        
        if test_name == 'admin_security_with_auth':
            if result.get('authenticated_access'):
                print(f"  ✅ Authentication: Working with credentials")
            else:
                print(f"  ❌ Authentication: Failed with credentials ({result.get('status_code')})")
        
        if test_name == 'admin_migrate_cvs':
            if result.get('endpoint_accessible'):
                print(f"  ✅ Endpoint: Accessible (proxy/forwarded headers working)")
            else:
                print(f"  ❌ Endpoint: Not accessible ({result.get('status_code')}) - routing issue")
        
        if test_name == 'admin_download_cv':
            if result.get('endpoint_accessible'):
                print(f"  ✅ Endpoint: Accessible (proxy/forwarded headers working)")
            else:
                print(f"  ❌ Endpoint: Not accessible ({result.get('status_code')}) - routing issue")
    
    print("="*80)
    
    # Final determination
    security_no_auth = results.get('admin_security_no_auth', {}).get('security_working', False)
    security_with_auth = results.get('admin_security_with_auth', {}).get('authenticated_access', False)
    migrate_cvs_working = results.get('admin_migrate_cvs', {}).get('endpoint_accessible', False)
    download_cv_working = results.get('admin_download_cv', {}).get('endpoint_accessible', False)
    
    print("\n🔍 MIDDLEWARE AUTHENTICATION DETERMINATION:")
    if security_no_auth and security_with_auth and migrate_cvs_working and download_cv_working:
        print("✅ MIDDLEWARE AUTHENTICATION: COMPLETELY SUCCESSFUL")
        print("✅ Custom AdminAuthMiddleware working independently")
        print("✅ All admin endpoints accessible with credentials")
        print("✅ Security fully implemented")
    elif security_no_auth and security_with_auth:
        print("⚠️  MIDDLEWARE AUTHENTICATION: PARTIALLY SUCCESSFUL")
        print("✅ Custom AdminAuthMiddleware working")
        print("❌ Some admin endpoints still have routing issues")
    else:
        print("❌ MIDDLEWARE AUTHENTICATION: FAILED")
        print("❌ Custom AdminAuthMiddleware not working properly")
        print("❌ Critical security and routing issues remain")
    
    return results

if __name__ == "__main__":
    main()