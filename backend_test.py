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
    
    def run_complete_external_tests(self):
        """Run complete external tests as requested by user"""
        logger.info("=== STARTING COMPLETE EXTERNAL TESTS ===")
        logger.info(f"Testing against: {self.base_url}")
        logger.info("=== CRITICAL CONTEXT ===")
        logger.info("- Final external verification for Pymetra")
        logger.info("- Testing updated admin panel with CV download/migration")
        logger.info("- Testing complete registration flow")
        logger.info("- Verifying Joan receives email and data goes to Google Sheets/Drive")
        
        results = {}
        
        # Test 1: OAuth Status
        logger.info("\n" + "="*60)
        results['oauth_status'] = self.test_auth_status()
        
        # Test 2: Database Count (before registration)
        logger.info("\n" + "="*60)
        results['database_count_before'] = self.test_database_count()
        
        # Test 3: Updated Admin Panel
        logger.info("\n" + "="*60)
        results['admin_panel_updated'] = self.test_admin_panel_updated()
        
        # Test 4: CV Migration
        logger.info("\n" + "="*60)
        results['cv_migration'] = self.test_cv_migration()
        
        # Test 5: Complete External Registration
        logger.info("\n" + "="*60)
        results['external_registration'] = self.test_external_registration_final()
        
        # Test 6: Database Count (after registration)
        logger.info("\n" + "="*60)
        results['database_count_after'] = self.test_database_count()
        
        logger.info("\n" + "="*60)
        logger.info("=== COMPLETE EXTERNAL TEST RESULTS SUMMARY ===")
        for test_name, result in results.items():
            status = "✅ PASS" if result.get('success') else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
            if not result.get('success'):
                logger.error(f"  Error: {result.get('error', 'Unknown error')}")
        
        # Critical Analysis
        logger.info("\n" + "="*60)
        logger.info("=== CRITICAL FINAL ANALYSIS ===")
        
        oauth_status = results.get('oauth_status', {})
        admin_panel = results.get('admin_panel_updated', {})
        migration = results.get('cv_migration', {})
        registration = results.get('external_registration', {})
        
        # OAuth Status
        if oauth_status.get('authenticated'):
            logger.info("✅ OAuth Status: AUTHENTICATED")
        else:
            logger.info("❌ OAuth Status: NOT AUTHENTICATED")
        
        # Admin Panel Features
        if admin_panel.get('success'):
            if admin_panel.get('has_download_cv') and admin_panel.get('has_migrate_cvs'):
                logger.info("✅ Admin Panel: NEW FEATURES PRESENT")
            else:
                logger.info("⚠️  Admin Panel: MISSING SOME NEW FEATURES")
        else:
            logger.info("❌ Admin Panel: NOT ACCESSIBLE")
        
        # CV Migration
        if migration.get('success'):
            logger.info(f"✅ CV Migration: WORKING (Migrated: {migration.get('migrated', 0)}, Total: {migration.get('total', 0)})")
        else:
            logger.info("❌ CV Migration: FAILED")
        
        # Registration
        if registration.get('success'):
            if registration.get('google_apis_working'):
                logger.info("✅ Registration: GOOGLE APIS CONFIRMED WORKING")
                logger.info("✅ Joan should receive email notification")
                logger.info("✅ Data should be in Google Sheets")
                logger.info("✅ CV should be in Google Drive")
            elif registration.get('email_sent') and registration.get('cv_saved'):
                logger.info("⚠️  Registration: WORKING BUT UNCLEAR IF GOOGLE OR BACKUP")
            else:
                logger.info("❌ Registration: NOT WORKING PROPERLY")
        else:
            logger.info("❌ Registration: FAILED")
        
        return results

def main():
    """Main test execution - Complete External Testing"""
    tester = PymetraBackendTester()
    results = tester.run_complete_external_tests()
    
    # Print final summary
    print("\n" + "="*80)
    print("PYMETRA COMPLETE EXTERNAL TEST RESULTS")
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
        if test_name == 'oauth_status' and result.get('success'):
            auth_data = result.get('data', {})
            print(f"  Authenticated: {auth_data.get('authenticated', False)}")
        
        if test_name == 'admin_panel_updated' and result.get('success'):
            print(f"  Has CV Download: {result.get('has_download_cv', False)}")
            print(f"  Has CV Migration: {result.get('has_migrate_cvs', False)}")
            print(f"  Has Google Drive: {result.get('has_google_drive', False)}")
        
        if test_name == 'cv_migration' and result.get('success'):
            print(f"  Migrated: {result.get('migrated', 0)}")
            print(f"  Already in Drive: {result.get('already_in_drive', 0)}")
            print(f"  Failed: {result.get('failed', 0)}")
            print(f"  Total: {result.get('total', 0)}")
        
        if test_name == 'external_registration' and result.get('success'):
            reg_data = result.get('data', {})
            print(f"  Registration ID: {reg_data.get('registration_id', 'N/A')}")
            print(f"  Email Sent: {result.get('email_sent', False)}")
            print(f"  CV Saved: {result.get('cv_saved', False)}")
            print(f"  Google APIs Working: {result.get('google_apis_working', False)}")
            print(f"  Joan Email Expected: {result.get('joan_email_expected', False)}")
            print(f"  Google Sheets Expected: {result.get('google_sheets_expected', False)}")
            print(f"  Google Drive Expected: {result.get('google_drive_expected', False)}")
        
        if 'database_count' in test_name and result.get('success'):
            count = result.get('count', 0)
            print(f"  Total Registrations: {count}")
    
    print("="*80)
    
    # Final determination
    oauth_authenticated = results.get('oauth_status', {}).get('authenticated', False)
    admin_features = results.get('admin_panel_updated', {}).get('success', False)
    migration_working = results.get('cv_migration', {}).get('success', False)
    registration_success = results.get('external_registration', {}).get('success', False)
    google_apis_working = results.get('external_registration', {}).get('google_apis_working', False)
    
    print("\n🔍 FINAL DETERMINATION:")
    if oauth_authenticated and admin_features and migration_working and registration_success and google_apis_working:
        print("✅ COMPLETE SYSTEM WORKING PERFECTLY")
        print("✅ Joan should receive email at joan@pymetra.com")
        print("✅ Data should appear in Google Sheets: 1aSMXxycQLw0aSwFE87Pg_cRS8nlbc51-nl95G7WaujE")
        print("✅ CV should appear in Google Drive: 186gcyPs1V2iUqB9CW5nRDB1H0G0I9a1v")
    elif oauth_authenticated and registration_success:
        print("⚠️  SYSTEM MOSTLY WORKING - SOME FEATURES MAY NEED VERIFICATION")
    else:
        print("❌ SYSTEM HAS CRITICAL ISSUES")
    
    return results

if __name__ == "__main__":
    main()