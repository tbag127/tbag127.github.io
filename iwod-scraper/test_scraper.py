import json
from scraper import extract_data, send_data

def test_workflow():
    """Test the complete workflow including data extraction and DingTalk sending"""
    print('Testing data extraction...')
    data = extract_data()
    print(f'Extracted data: {json.dumps(data, indent=2, ensure_ascii=False)}')

    print('\nTesting DingTalk message sending...')
    send_data(data)

if __name__ == "__main__":
    test_workflow()
