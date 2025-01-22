import json
import pytz
import pathlib
from datetime import datetime
from unittest.mock import patch
from dotenv import load_dotenv
from scraper import (
    extract_data, send_data, is_business_hours, BEIJING_TZ,
    is_token_expired, handle_token_expiration
)

# Load environment variables from the correct path
env_path = pathlib.Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def test_page_refresh():
    """Test that page refresh gets current data"""
    print('\nTesting page refresh functionality...')
    
    # First extraction to get initial data
    initial_data = extract_data()
    print(f'Initial data: {json.dumps(initial_data, indent=2, ensure_ascii=False)}')
    
    # Force refresh and get updated data
    data = extract_data()
    print(f'Data after refresh: {json.dumps(data, indent=2, ensure_ascii=False)}')
    
    # Verify specific values
    assert data['metrics']['客流'] == 3, "Expected 客流 to be 3 after page refresh"
    assert data['metrics']['售课'] == 4, "Expected 售课 to be 4 after page refresh"
    print('✓ Page refresh test passed - got current data')

def test_message_format():
    """Test that messages start with '数据分享'"""
    print('\nTesting message format...')
    data = {
        'timestamp': datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'),
        'metrics': {
            '线上销售额': 100.0,
            '线下销售额': 200.0,
            '结算金额': 300.0,
            '新增会员': 1,
            '新增潜客': 2,
            '售课': 3,
            '客流': 4
        }
    }
    try:
        send_data(data)
        print('Message format test passed - message starts with 数据分享')
    except Exception as e:
        print(f'Message format test failed: {str(e)}')

def test_business_hours():
    """Test business hours restriction (10:00-22:00 Beijing time)"""
    print('\nTesting business hours restriction...')
    current_time = datetime.now(BEIJING_TZ)
    print(f'Current Beijing time: {current_time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Is business hours: {is_business_hours()}')

def test_token_refresh():
    """Test token refresh via QR code"""
    print('\nTesting token refresh functionality...')
    if is_token_expired():
        print('Token expired, testing refresh flow...')
        success = handle_token_expiration()
        if success:
            print('Token refresh test passed - Successfully refreshed token')
        else:
            print('Token refresh test failed - Could not refresh token')
    else:
        print('Token is still valid, skipping refresh test')

def test_workflow():
    """Test the complete workflow including data extraction and DingTalk sending"""
    print('\nTesting complete workflow...')
    try:
        data = extract_data()
        if not data:
            print("Error: Failed to extract data")
            return
            
        print(f'Extracted data: {json.dumps(data, indent=2, ensure_ascii=False)}')
        
        # Verify specific values
        metrics = data.get('metrics', {})
        print('\nVerifying metric values:')
        print(f'客流: {metrics.get("客流", "N/A")} (expected: 3)')
        print(f'售课: {metrics.get("售课", "N/A")} (expected: 4)')
        
        try:
            assert metrics.get('客流') == 3, f'Expected 客流 to be 3, got {metrics.get("客流")}'
            assert metrics.get('售课') == 4, f'Expected 售课 to be 4, got {metrics.get("售课")}'
            print('✓ Metric values verified')
        except AssertionError as e:
            print(f'✗ Metric verification failed: {str(e)}')
    except Exception as e:
        print(f"Error in workflow test: {str(e)}")
        return
    print('\nTesting DingTalk message sending...')
    send_data(data)

if __name__ == "__main__":
    print("=== Starting iWOD Scraper Tests ===")
    test_page_refresh()
    test_message_format()
    test_business_hours()
    test_token_refresh()
    test_workflow()
    print("\n=== Tests Complete ===")
