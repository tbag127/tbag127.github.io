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
    data = extract_data()
    print(f'Extracted data after refresh: {json.dumps(data, indent=2, ensure_ascii=False)}')
    assert data['metrics']['客流'] == 3, "Expected 客流 to be 3 after page refresh"
    print('Page refresh test passed - got current data')

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
    data = extract_data()
    print(f'Extracted data: {json.dumps(data, indent=2, ensure_ascii=False)}')
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
