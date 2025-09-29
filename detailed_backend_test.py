#!/usr/bin/env python3
"""
Detailed Backend Testing for Pymetra Production Issues
Focus on Google APIs integration debugging
"""

import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://pymetra.com"

def test_detailed_registration():
    """Detailed registration test with comprehensive logging capture"""
    logger.info("=== DETAILED REGISTRATION TEST ===")
    
    # Create minimal test PDF
    pdf_content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 44>>stream
BT/F1 12 Tf 100 700 Td(Test CV Pymetra)Tj ET
endstream endobj
xref 0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer<</Size 5/Root 1 0 R>>
startxref 300
%%EOF"""
    
    # Test data
    form_data = {
        'fullName': 'TestAgent Pymetra Production',
        'email': 'test.production@pymetra.com',
        'geographicArea': 'España',
        'mainSector': 'Tecnología',
        'language': 'es'
    }
    
    files = {
        'cv': ('test_cv_production.pdf', pdf_content, 'application/pdf')
    }
    
    try:
        logger.info(f"Sending registration to: {BASE_URL}/api/register-agent")
        logger.info(f"Form data: {form_data}")
        logger.info(f"PDF size: {len(pdf_content)} bytes")
        
        response = requests.post(
            f"{BASE_URL}/api/register-agent",
            data=form_data,
            files=files,
            timeout=60
        )
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'registration_id': data.get('registration_id'),
                'email_sent': data.get('email_sent'),
                'cv_saved': data.get('cv_saved'),
                'message': data.get('message'),
                'full_response': data
            }
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text,
                'headers': dict(response.headers)
            }
            
    except Exception as e:
        logger.error(f"Registration test failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_auth_details():
    """Detailed authentication test"""
    logger.info("=== DETAILED AUTH TEST ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/status", timeout=30)
        logger.info(f"Auth Status Code: {response.status_code}")
        logger.info(f"Auth Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'authenticated': data.get('authenticated'),
                'message': data.get('message'),
                'login_url': data.get('login_url'),
                'error': data.get('error'),
                'full_response': data
            }
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text
            }
            
    except Exception as e:
        logger.error(f"Auth test failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_database_details():
    """Detailed database test"""
    logger.info("=== DETAILED DATABASE TEST ===")
    
    try:
        # Test count
        response = requests.get(f"{BASE_URL}/api/registrations/count", timeout=30)
        logger.info(f"DB Count Status: {response.status_code}")
        logger.info(f"DB Count Response: {response.text}")
        
        count_result = None
        if response.status_code == 200:
            count_result = response.json()
        
        # Test registrations list
        response2 = requests.get(f"{BASE_URL}/api/registrations?limit=5", timeout=30)
        logger.info(f"DB List Status: {response2.status_code}")
        logger.info(f"DB List Response: {response2.text}")
        
        list_result = None
        if response2.status_code == 200:
            list_result = response2.json()
        
        return {
            'success': True,
            'count_result': count_result,
            'list_result': list_result,
            'total_registrations': count_result.get('total_registrations', 0) if count_result else 0
        }
        
    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_available_endpoints():
    """Test what endpoints are actually available"""
    logger.info("=== TESTING AVAILABLE ENDPOINTS ===")
    
    endpoints_to_test = [
        "/api/health",
        "/api/auth/status", 
        "/api/admin/",
        "/api/admin/test-integrations",
        "/api/registrations/count",
        "/api/registrations"
    ]
    
    results = {}
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, timeout=30)
            
            results[endpoint] = {
                'status_code': response.status_code,
                'available': response.status_code != 404,
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.text)
            }
            
            logger.info(f"{endpoint}: {response.status_code} ({'✅' if response.status_code != 404 else '❌'})")
            
        except Exception as e:
            results[endpoint] = {
                'status_code': 'ERROR',
                'available': False,
                'error': str(e)
            }
            logger.error(f"{endpoint}: ERROR - {str(e)}")
    
    return results

def main():
    """Run detailed tests"""
    logger.info("=== STARTING DETAILED PYMETRA BACKEND ANALYSIS ===")
    logger.info(f"Testing production environment: {BASE_URL}")
    
    results = {}
    
    # Test 1: Available endpoints
    logger.info("\n1. Testing endpoint availability...")
    results['endpoints'] = test_available_endpoints()
    
    # Test 2: Authentication details
    logger.info("\n2. Testing authentication details...")
    results['auth'] = test_auth_details()
    
    # Test 3: Database details
    logger.info("\n3. Testing database details...")
    results['database'] = test_database_details()
    
    # Test 4: Registration with full debugging
    logger.info("\n4. Testing registration with debugging...")
    results['registration'] = test_detailed_registration()
    
    # Summary
    logger.info("\n=== DETAILED TEST SUMMARY ===")
    
    print("\n" + "="*80)
    print("PYMETRA PRODUCTION BACKEND ANALYSIS")
    print("="*80)
    
    # Endpoint availability
    print("\n📡 ENDPOINT AVAILABILITY:")
    for endpoint, result in results['endpoints'].items():
        status = "✅ Available" if result['available'] else "❌ Not Found"
        print(f"  {endpoint}: {status} ({result['status_code']})")
    
    # Authentication status
    print(f"\n🔐 AUTHENTICATION:")
    auth = results['auth']
    if auth['success']:
        auth_status = "✅ Authenticated" if auth['authenticated'] else "❌ Not Authenticated"
        print(f"  Status: {auth_status}")
        print(f"  Message: {auth.get('message', 'N/A')}")
        if auth.get('error'):
            print(f"  Error: {auth['error']}")
    else:
        print(f"  ❌ Auth test failed: {auth.get('error', 'Unknown error')}")
    
    # Database status
    print(f"\n💾 DATABASE:")
    db = results['database']
    if db['success']:
        count = db.get('total_registrations', 0)
        print(f"  Total registrations: {count}")
        print(f"  Database connection: ✅ Working")
    else:
        print(f"  ❌ Database test failed: {db.get('error', 'Unknown error')}")
    
    # Registration test
    print(f"\n📝 REGISTRATION TEST:")
    reg = results['registration']
    if reg['success']:
        print(f"  ✅ Registration successful")
        print(f"  Registration ID: {reg.get('registration_id', 'N/A')}")
        print(f"  Email sent: {'✅' if reg.get('email_sent') else '❌'}")
        print(f"  CV saved: {'✅' if reg.get('cv_saved') else '❌'}")
        print(f"  Message: {reg.get('message', 'N/A')}")
    else:
        print(f"  ❌ Registration failed")
        print(f"  Status code: {reg.get('status_code', 'N/A')}")
        print(f"  Error: {reg.get('error', 'Unknown error')}")
    
    print("\n" + "="*80)
    
    return results

if __name__ == "__main__":
    main()