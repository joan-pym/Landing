#!/usr/bin/env python3
"""
Detailed OAuth Verification Test for Pymetra
Focuses on the specific user request to verify Google APIs after OAuth
"""

import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://pymetra.com"

def test_detailed_oauth_status():
    """Test 1: Detailed OAuth Status Check"""
    logger.info("=== TEST 1: DETAILED OAUTH STATUS ===")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/status", timeout=30)
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("=== OAUTH STATUS DETAILS ===")
            logger.info(f"Authenticated: {data.get('authenticated')}")
            logger.info(f"Message: {data.get('message')}")
            logger.info(f"Login URL: {data.get('login_url')}")
            logger.info(f"Full Response: {json.dumps(data, indent=2)}")
            return {'success': True, 'data': data}
        else:
            logger.error(f"OAuth status failed: {response.status_code} - {response.text}")
            return {'success': False, 'error': f"HTTP {response.status_code}"}
    except Exception as e:
        logger.error(f"OAuth status test failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_immediate_registration():
    """Test 2: Immediate Registration with User's Exact Data"""
    logger.info("=== TEST 2: IMMEDIATE REGISTRATION TEST ===")
    
    # Create minimal PDF
    pdf_content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 44>>stream
BT/F1 12 Tf 100 700 Td(Test OAuth Final CV)Tj ET
endstream endobj
xref 0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer<</Size 5/Root 1 0 R>>startxref 300 %%EOF"""
    
    try:
        # User's exact data
        form_data = {
            'fullName': 'Test OAuth Verificación Final',
            'email': 'test.oauth.final@pymetra.com',
            'geographicArea': 'Madrid',
            'mainSector': 'Consultoría',
            'language': 'es'
        }
        
        files = {
            'cv': ('test_oauth_final.pdf', pdf_content, 'application/pdf')
        }
        
        logger.info("=== SENDING REGISTRATION REQUEST ===")
        logger.info(f"Data: {form_data}")
        logger.info(f"PDF Size: {len(pdf_content)} bytes")
        
        # Send with extended timeout for Google APIs
        response = requests.post(
            f"{BASE_URL}/api/register-agent",
            data=form_data,
            files=files,
            timeout=120  # 2 minutes for Google APIs
        )
        
        logger.info("=== REGISTRATION RESPONSE ===")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        logger.info(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("=== REGISTRATION SUCCESS ===")
            logger.info(f"Full Response: {json.dumps(data, indent=2)}")
            
            # Analyze response for Google APIs indicators
            message = data.get('message', '')
            email_sent = data.get('email_sent', False)
            cv_saved = data.get('cv_saved', False)
            registration_id = data.get('registration_id')
            
            logger.info("=== GOOGLE APIS ANALYSIS ===")
            logger.info(f"Registration ID: {registration_id}")
            logger.info(f"Message: {message}")
            logger.info(f"Email Sent: {email_sent}")
            logger.info(f"CV Saved: {cv_saved}")
            
            # Determine if Google APIs worked
            google_working = False
            if 'Google Sheets' in message and 'Drive' in message:
                google_working = True
                logger.info("✅ GOOGLE APIS CONFIRMED: Message mentions Google Sheets and Drive")
            elif email_sent and cv_saved:
                logger.info("⚠️  APIS WORKING: Email sent and CV saved, but unclear if Google or backup")
            else:
                logger.info("❌ GOOGLE APIS LIKELY FAILED: Limited functionality")
            
            return {
                'success': True,
                'data': data,
                'google_apis_working': google_working,
                'analysis': {
                    'registration_id': registration_id,
                    'email_sent': email_sent,
                    'cv_saved': cv_saved,
                    'message': message,
                    'response_time': response.elapsed.total_seconds()
                }
            }
        else:
            logger.error("=== REGISTRATION FAILED ===")
            logger.error(f"Status: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return {
                'success': False,
                'error': f"HTTP {response.status_code}",
                'response': response.text
            }
            
    except Exception as e:
        logger.error(f"=== REGISTRATION EXCEPTION ===")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Type: {type(e).__name__}")
        return {'success': False, 'error': str(e)}

def test_database_increment():
    """Test 3: Database Registration Count"""
    logger.info("=== TEST 3: DATABASE COUNT ===")
    try:
        response = requests.get(f"{BASE_URL}/api/registrations/count", timeout=30)
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('total_registrations', 0)
            logger.info(f"Total Registrations: {count}")
            logger.info(f"Full Response: {json.dumps(data, indent=2)}")
            return {'success': True, 'count': count, 'data': data}
        else:
            logger.error(f"Database count failed: {response.status_code} - {response.text}")
            return {'success': False, 'error': f"HTTP {response.status_code}"}
    except Exception as e:
        logger.error(f"Database count test failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def main():
    """Run detailed OAuth verification tests"""
    logger.info("="*80)
    logger.info("PYMETRA OAUTH VERIFICATION - DETAILED ANALYSIS")
    logger.info("="*80)
    logger.info("CONTEXT: User completed OAuth, /api/auth/status shows authenticated: true")
    logger.info("ISSUE: oauth_credentials.json doesn't exist physically")
    logger.info("GOAL: Verify if Google APIs actually work after OAuth")
    logger.info("="*80)
    
    results = {}
    
    # Test 1: OAuth Status
    results['oauth_status'] = test_detailed_oauth_status()
    
    # Test 2: Database count before
    results['db_before'] = test_database_increment()
    
    # Test 3: Critical registration test
    results['registration'] = test_immediate_registration()
    
    # Test 4: Database count after
    results['db_after'] = test_database_increment()
    
    # Final Analysis
    logger.info("="*80)
    logger.info("FINAL OAUTH VERIFICATION ANALYSIS")
    logger.info("="*80)
    
    oauth_auth = results.get('oauth_status', {}).get('data', {}).get('authenticated', False)
    reg_success = results.get('registration', {}).get('success', False)
    google_working = results.get('registration', {}).get('google_apis_working', False)
    
    db_before = results.get('db_before', {}).get('count', 0)
    db_after = results.get('db_after', {}).get('count', 0)
    db_incremented = db_after > db_before
    
    logger.info(f"OAuth Authenticated: {oauth_auth}")
    logger.info(f"Registration Success: {reg_success}")
    logger.info(f"Google APIs Working: {google_working}")
    logger.info(f"Database Incremented: {db_incremented} ({db_before} -> {db_after})")
    
    if oauth_auth and reg_success and google_working and db_incremented:
        logger.info("🎉 CONCLUSION: OAUTH AND GOOGLE APIS ARE FULLY FUNCTIONAL")
        conclusion = "FULLY_FUNCTIONAL"
    elif oauth_auth and reg_success and db_incremented:
        logger.info("⚠️  CONCLUSION: OAUTH WORKS, GOOGLE APIS STATUS UNCLEAR")
        conclusion = "PARTIALLY_FUNCTIONAL"
    elif oauth_auth:
        logger.info("❌ CONCLUSION: OAUTH AUTHENTICATED BUT REGISTRATION ISSUES")
        conclusion = "OAUTH_ONLY"
    else:
        logger.info("❌ CONCLUSION: OAUTH NOT WORKING")
        conclusion = "NOT_FUNCTIONAL"
    
    logger.info("="*80)
    
    return {
        'results': results,
        'conclusion': conclusion,
        'summary': {
            'oauth_authenticated': oauth_auth,
            'registration_success': reg_success,
            'google_apis_working': google_working,
            'database_incremented': db_incremented,
            'registrations_before': db_before,
            'registrations_after': db_after
        }
    }

if __name__ == "__main__":
    main()