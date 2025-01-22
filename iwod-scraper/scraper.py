import os
import sys
import time
import json
import pytz
import requests
import logging
from datetime import datetime
from browser_automation import navigate_browser, run_javascript_browser, view_browser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Beijing timezone for time checks
BEIJING_TZ = pytz.timezone('Asia/Shanghai')
BUSINESS_START_HOUR = 10  # 10:00 AM Beijing time
BUSINESS_END_HOUR = 22    # 10:00 PM Beijing time

def is_token_expired():
    """
    Check if the current session token is expired
    Returns True if token is expired, False otherwise
    """
    try:
        # Check current URL for QR login redirect
        js_script = """
        const currentUrl = window.location.href;
        console.log('Current URL:', currentUrl);
        currentUrl;
        """
        current_url = run_javascript_browser(js_script)
        
        if 'qrconnect' in current_url.lower():
            logging.warning("Token expired: Redirected to QR login page")
            return True
            
        # Try to access a protected element to verify authentication
        js_script = """
        try {
            const element = document.querySelector('p[devinid="54"]');
            return element ? true : false;
        } catch (e) {
            console.error('Error accessing protected element:', e);
            return false;
        }
        """
        element_exists = run_javascript_browser(js_script)
        
        if not element_exists:
            logging.warning("Token expired: Cannot access protected elements")
            return True
            
        return False
    except Exception as e:
        logging.error(f"Error checking token expiration: {str(e)}")
        return True

def store_auth_state():
    """
    Store authentication state information
    Returns dict with auth state details
    """
    try:
        # Get all cookies
        js_script = """
        const cookies = document.cookie.split(';').reduce((acc, cookie) => {
            const [key, value] = cookie.trim().split('=');
            acc[key] = value;
            return acc;
        }, {});
        console.log('Cookies:', cookies);
        cookies;
        """
        cookies = run_javascript_browser(js_script)
        
        # Get localStorage items
        js_script = """
        const storage = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            storage[key] = localStorage.getItem(key);
        }
        console.log('LocalStorage:', storage);
        storage;
        """
        storage = run_javascript_browser(js_script)
        
        # Get current URL
        js_script = """
        window.location.href;
        """
        current_url = run_javascript_browser(js_script)
        
        auth_state = {
            'timestamp': datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'),
            'url': current_url,
            'cookies': cookies,
            'storage': storage
        }
        
        logging.info(f"Stored authentication state at {auth_state['timestamp']}")
        return auth_state
    except Exception as e:
        logging.error(f"Error storing authentication state: {str(e)}")
        return None

def wait_for_login_success(timeout=300):  # 5 minutes timeout
    """
    Wait for successful login after QR code scan
    Returns True if login successful, False if timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Check if we're back on the main page
        js_script = """
        const currentUrl = window.location.href;
        console.log('Current URL:', currentUrl);
        currentUrl.includes('/admin/dataAnalysis/storeSummary');
        """
        if run_javascript_browser(js_script):
            logging.info("Login successful - returned to dashboard")
            # Store authentication state after successful login
            auth_state = store_auth_state()
            if auth_state:
                logging.info("Authentication state stored successfully")
            return True
            
        # Check if we can access protected elements
        js_script = """
        try {
            const element = document.querySelector('p[devinid="54"]');
            return element ? true : false;
        } catch (e) {
            return false;
        }
        """
        if run_javascript_browser(js_script):
            logging.info("Login successful - can access protected elements")
            # Store authentication state after successful login
            auth_state = store_auth_state()
            if auth_state:
                logging.info("Authentication state stored successfully")
            return True
            
        time.sleep(5)  # Check every 5 seconds
        
    logging.error(f"Login timeout after {timeout} seconds")
    return False

def handle_token_expiration():
    """
    Handle expired token by initiating QR code login flow
    Returns True if login successful, False otherwise
    """
    try:
        logging.info("Initiating QR code login flow")
        
        # Navigate to QR code login page
        navigate_browser('https://www.iwod.cn/qrconnect/')
        
        # Wait for QR code to be displayed
        time.sleep(5)
        
        # Notify user to scan QR code
        logging.warning("QR code displayed - Please scan with WeChat")
        
        # Wait for successful login
        if wait_for_login_success():
            # Navigate back to dashboard
            navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
            return True
            
        return False
    except Exception as e:
        logging.error(f"Error in handle_token_expiration: {str(e)}")
        return False

def extract_data():
    """
    Extract data from the iWOD dashboard using browser commands
    Returns a dictionary containing the scraped data
    """
    try:
        # Navigate to the dashboard using Devin browser command
        navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
        
        # Check if token is expired
        if is_token_expired():
            logging.info("Token expired, attempting to refresh")
            if not handle_token_expiration():
                raise Exception("Failed to refresh token")
        
        # Execute JavaScript to extract data using specific devinids
        js_script = """
        const metrics = {};
        metrics['线上销售额元'] = document.querySelector('p[devinid="54"]').textContent;
        metrics['线下销售额元'] = document.querySelector('p[devinid="59"]').textContent;
        metrics['结算金额元'] = document.querySelector('p[devinid="64"]').textContent;
        metrics['新增会员人'] = document.querySelector('p[devinid="69"]').textContent;
        metrics['新增潜客人'] = document.querySelector('p[devinid="74"]').textContent;
        metrics['售课节'] = document.querySelector('p[devinid="79"]').textContent;
        metrics['客流人次'] = document.querySelector('p[devinid="84"]').textContent;
        console.log(JSON.stringify(metrics, null, 2));
        metrics;
        """
        
        result = run_javascript_browser(js_script)
        
        # Parse the extracted data
        metrics = json.loads(result)
        data = {
            'timestamp': datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'),
            'metrics': {
                '线上销售额': float(metrics.get('线上销售额元', 0)),
                '线下销售额': float(metrics.get('线下销售额元', 0)),
                '结算金额': float(metrics.get('结算金额元', 0)),
                '新增会员': int(metrics.get('新增会员人', 0)),
                '新增潜客': int(metrics.get('新增潜客人', 0)),
                '售课': int(metrics.get('售课节', 0)),
                '客流': int(metrics.get('客流人次', 0))
            }
        }
        return data
        
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        # Return default data structure with zeros
        return {
            'timestamp': datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'),
            'metrics': {
                '线上销售额': 0,
                '线下销售额': 0,
                '结算金额': 0,
                '新增会员': 0,
                '新增潜客': 0,
                '售课': 0,
                '客流': 0
            }
        }

def send_data(data):
    """
    Send the extracted data via DingTalk webhook
    """
    webhook_url = os.getenv('DINGTALK_WEBHOOK_URL')
    if not webhook_url:
        logging.error("DINGTALK_WEBHOOK_URL environment variable not set")
        raise Exception("Missing webhook URL configuration")
    
    # Format the message with required prefix and Beijing time
    metrics = data['metrics']
    beijing_time = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    message = f"数据分享 - 健身房数据统计 ({beijing_time})\n\n"
    message += f"• 线上销售额: ¥{metrics['线上销售额']:.2f}\n"
    message += f"• 线下销售额: ¥{metrics['线下销售额']:.2f}\n"
    message += f"• 结算金额: ¥{metrics['结算金额']:.2f}\n"
    message += f"• 新增会员: {metrics['新增会员']}人\n"
    message += f"• 新增潜客: {metrics['新增潜客']}人\n"
    message += f"• 售课数量: {metrics['售课']}节\n"
    message += f"• 客流量: {metrics['客流']}人次\n"
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logging.info(f"Data sent successfully to DingTalk at {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to DingTalk: {str(e)}")
        raise  # Propagate error for retry logic

def is_business_hours():
    """Check if current time is within Beijing business hours (10:00-22:00)"""
    beijing_time = datetime.now(BEIJING_TZ)
    return BUSINESS_START_HOUR <= beijing_time.hour < BUSINESS_END_HOUR

def job(max_retries=3):
    """
    Main job to run hourly
    Only sends data during Beijing business hours (10:00-22:00)
    Includes retry logic for token expiration
    """
    try:
        if not is_business_hours():
            logging.info(f"Outside of business hours (Beijing time: {datetime.now(BEIJING_TZ)})")
            return

        retry_count = 0
        while retry_count < max_retries:
            try:
                data = extract_data()
                send_data(data)
                logging.info(f"Data extracted and sent successfully at {datetime.now(BEIJING_TZ)}")
                return  # Success, exit the retry loop
            except Exception as e:
                retry_count += 1
                if "Token expired" in str(e) and retry_count < max_retries:
                    logging.warning(f"Token expired, attempt {retry_count} of {max_retries}")
                    time.sleep(5)  # Wait before retry
                    continue
                elif retry_count >= max_retries:
                    logging.error(f"Max retries ({max_retries}) exceeded")
                    raise
                else:
                    logging.error(f"Error occurred: {str(e)}")
                    raise
    except Exception as e:
        logging.error(f"Critical error in job: {str(e)}")

def main():
    """
    Main function to run the scraper once.
    Systemd service will handle scheduling.
    """
    try:
        job()
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
