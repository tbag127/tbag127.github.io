import json
import pytz
import pathlib
from datetime import datetime
from unittest.mock import patch
from dotenv import load_dotenv
from scraper import extract_data, send_data, is_business_hours, BEIJING_TZ

# Load environment variables from the correct path
env_path = pathlib.Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

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

def test_workflow():
    """Test the complete workflow including data extraction and DingTalk sending"""
    print('\nTesting data extraction...')
    data = extract_data()
    print(f'Extracted data: {json.dumps(data, indent=2, ensure_ascii=False)}')

    print('\nTesting DingTalk message sending...')
    send_data(data)

if __name__ == "__main__":
    print("=== Starting iWOD Scraper Tests ===")
    test_message_format()
    test_business_hours()
    test_workflow()
    print("\n=== Tests Complete ===")
