#!/usr/bin/env python3
"""
Backend Testing Suite for Pymetra
Tests critical Google APIs integration issues in production
"""

import requests
import json
import logging
import tempfile
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Production URL
BASE_URL = "https://pymetra.com"

class PymetraBackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pymetra-Backend-Tester/1.0'
        })
        
    def test_auth_status(self):
        """Test 1: Google APIs Authentication Status"""
        logger.info("=== TEST 1: Authentication Status ===")
        try:
            response = self.session.get(f"{self.base_url}/api/auth/status", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                is_authenticated = data.get('authenticated', False)
                logger.info(f"Google APIs Authenticated: {is_authenticated}")
                return {
                    'success': True,
                    'authenticated': is_authenticated,
                    'data': data
                }
            else:
                logger.error(f"Auth status check failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Auth status test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_integrations_endpoint(self):
        """Test 2: Test Integrations Endpoint"""
        logger.info("=== TEST 2: Test Integrations ===")
        try:
            response = self.session.get(f"{self.base_url}/api/admin/test-integrations", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info("Integration Test Results:")
                for test_name, result in data.get('tests', {}).items():
                    logger.info(f"  {test_name}: {result}")
                return {'success': True, 'data': data}
            else:
                logger.error(f"Integrations test failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Integrations test failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def test_database_count(self):
        """Test 3: Database Registration Count"""
        logger.info("=== TEST 3: Database Count ===")
        try:
            response = self.session.get(f"{self.base_url}/api/registrations/count", timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('total_registrations', 0)
                logger.info(f"Total registrations in database: {count}")
                return {'success': True, 'count': count, 'data': data}
            else:
                logger.error(f"Database count test failed: {response.status_code}")
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Database count test failed: {str(e)}")
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
    
    def test_oauth_verification_registration(self):
        """Test 5: OAuth Verification Registration with Specific Data"""
        logger.info("=== TEST 5: OAuth Verification Registration ===")
        try:
            # Create test PDF
            pdf_content = self.create_test_pdf()
            if not pdf_content:
                return {'success': False, 'error': 'Could not create test PDF'}
            
            # Use EXACT data from user request
            form_data = {
                'fullName': 'Test OAuth Verificación Final',
                'email': 'test.oauth.final@pymetra.com',
                'geographicArea': 'Madrid',
                'mainSector': 'Consultoría',
                'language': 'es'
            }
            
            # Prepare file
            files = {
                'cv': ('test_oauth_final.pdf', pdf_content, 'application/pdf')
            }
            
            logger.info("=== OAUTH VERIFICATION TEST DATA ===")
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
                logger.info(f"Email sent (Google/SMTP): {data.get('email_sent')}")
                logger.info(f"CV saved (Drive/Local): {data.get('cv_saved')}")
                
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
                
                return {
                    'success': True, 
                    'data': data,
                    'google_apis_working': google_apis_working,
                    'email_sent': email_sent,
                    'cv_saved': cv_saved
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
            logger.error(f"=== OAUTH VERIFICATION TEST FAILED ===")
            logger.error(f"Exception: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            return {'success': False, 'error': str(e)}
    
    def run_all_tests(self):
        """Run all backend tests"""
        logger.info("=== STARTING PYMETRA BACKEND TESTS ===")
        logger.info(f"Testing against: {self.base_url}")
        
        results = {}
        
        # Test 1: Auth Status
        results['auth_status'] = self.test_auth_status()
        
        # Test 2: Integrations
        results['integrations'] = self.test_integrations_endpoint()
        
        # Test 3: Database Count
        results['database_count'] = self.test_database_count()
        
        # Test 4: Admin Panel
        results['admin_panel'] = self.test_admin_panel()
        
        # Test 5: Registration with Debugging
        results['registration'] = self.test_registration_with_debugging()
        
        logger.info("=== TEST RESULTS SUMMARY ===")
        for test_name, result in results.items():
            status = "✅ PASS" if result.get('success') else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
            if not result.get('success'):
                logger.error(f"  Error: {result.get('error', 'Unknown error')}")
        
        return results

def main():
    """Main test execution"""
    tester = PymetraBackendTester()
    results = tester.run_all_tests()
    
    # Print final summary
    print("\n" + "="*60)
    print("PYMETRA BACKEND TEST RESULTS")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get('success'))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print()
    
    for test_name, result in results.items():
        status = "✅ PASS" if result.get('success') else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
        if not result.get('success'):
            print(f"  Error: {result.get('error', 'Unknown error')}")
    
    print("="*60)
    
    return results

if __name__ == "__main__":
    main()