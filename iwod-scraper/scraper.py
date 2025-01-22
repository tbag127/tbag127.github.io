import os
import sys
import time
import json
import pytz
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from browser_automation import navigate_browser, run_javascript_browser, view_browser, get_browser_console

# Authentication monitoring
AUTH_ATTEMPT_LIMIT = 5  # Maximum number of failed attempts before extended cooldown
AUTH_COOLDOWN = 300  # 5 minutes cooldown after reaching attempt limit
auth_attempts = {
    'count': 0,
    'last_attempt': None,
    'cooldown_until': None
}

# Load environment variables from the correct path
import pathlib
env_path = pathlib.Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Add error log handler separately
error_handler = logging.FileHandler('scraper.error.log')
error_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(error_handler)

# Create logger
logger = logging.getLogger('iwod_scraper')

# Add authentication logger with separate file
auth_handler = logging.FileHandler('auth.log')
auth_handler.setLevel(logging.INFO)
auth_handler.setFormatter(logging.Formatter('%(asctime)s - AUTH - %(levelname)s - %(message)s'))

auth_logger = logging.getLogger('iwod_auth')
auth_logger.setLevel(logging.INFO)
auth_logger.addHandler(auth_handler)
auth_logger.addHandler(logging.StreamHandler())

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
            auth_logger.info("Login successful - returned to dashboard")
            # Store authentication state after successful login
            auth_state = store_auth_state()
            if auth_state:
                auth_logger.info("Authentication state stored successfully")
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
            auth_logger.info("Login successful - can access protected elements")
            # Store authentication state after successful login
            auth_state = store_auth_state()
            if auth_state:
                auth_logger.info("Authentication state stored successfully")
            return True
            
        time.sleep(5)  # Check every 5 seconds
        
    logging.error(f"Login timeout after {timeout} seconds")
    return False

def handle_token_expiration():
    """
    Handle expired token by initiating QR code login flow
    Returns True if login successful, False otherwise
    Includes authentication attempt monitoring and cooldown periods
    """
    try:
        # Check if we're in cooldown
        current_time = datetime.now(BEIJING_TZ)
        if auth_attempts['cooldown_until'] and current_time < auth_attempts['cooldown_until']:
            wait_time = (auth_attempts['cooldown_until'] - current_time).total_seconds()
            auth_logger.warning(f"Authentication in cooldown. Please wait {wait_time:.0f} seconds before next attempt.")
            return False

        # Update authentication attempts
        auth_attempts['count'] += 1
        auth_attempts['last_attempt'] = current_time
        
        if auth_attempts['count'] >= AUTH_ATTEMPT_LIMIT:
            auth_attempts['cooldown_until'] = current_time + timedelta(seconds=AUTH_COOLDOWN)
            auth_logger.error(
                f"Authentication attempt limit reached ({auth_attempts['count']}/{AUTH_ATTEMPT_LIMIT}). "
                f"Cooldown initiated until: {auth_attempts['cooldown_until'].strftime('%Y-%m-%d %H:%M:%S')}"
            )
            return False

        auth_logger.info(
            f"Initiating QR code login flow (Attempt {auth_attempts['count']}/{AUTH_ATTEMPT_LIMIT} "
            f"at {current_time.strftime('%Y-%m-%d %H:%M:%S')})"
        )
        
        # Navigate to QR code login page
        navigate_browser('https://www.iwod.cn/qrconnect/')
        
        # Wait for QR code to be displayed
        time.sleep(5)
        
        # Notify user to scan QR code
        auth_logger.warning(
            f"QR code displayed - Please scan with WeChat "
            f"(Attempt {auth_attempts['count']}/{AUTH_ATTEMPT_LIMIT})"
        )
        
        # Wait for successful login
        if wait_for_login_success():
            # Reset authentication attempts on success
            auth_attempts['count'] = 0
            auth_attempts['cooldown_until'] = None
            auth_logger.info(
                f"Authentication successful at {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')} "
                "- Authentication attempts reset"
            )
            
            # Navigate back to dashboard
            navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
            return True
        
        auth_logger.error(
            f"Authentication failed (Attempt {auth_attempts['count']}/{AUTH_ATTEMPT_LIMIT}) "
            f"at {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return False
            
    except Exception as e:
        auth_logger.error(
            f"Error in handle_token_expiration: {str(e)} "
            f"(Attempt {auth_attempts['count']}/{AUTH_ATTEMPT_LIMIT})"
        )
        return False

def extract_data():
    """
    Extract data from the iWOD dashboard using browser commands
    Returns a dictionary containing the scraped data
    """
    try:
        # Navigate to the dashboard and force reload
        url = 'https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5'
        navigate_browser(url)
        
        # Force page reload using JavaScript and verify
        logger.info("Forcing page reload to get fresh data")
        run_javascript_browser("window.location.reload(true);")
        time.sleep(5)  # Initial wait for reload
        
        # Verify page loaded correctly and wait for data
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Force page reload and wait
                logger.info("Forcing page reload")
                run_javascript_browser("window.location.reload(true);")
                time.sleep(5)  # Wait for reload
                
                # Check if elements are present and have values
                js_check = """
                function checkElements() {
                    const elements = {
                        '客流': document.querySelector('p[devinid="84"]'),
                        '销售': document.querySelector('p[devinid="54"]')
                    };
                    
                    const results = {};
                    Object.entries(elements).forEach(([key, el]) => {
                        if (!el) {
                            console.error(`Missing element: ${key}`);
                            results[key] = false;
                        } else {
                            const value = el.textContent.trim();
                            console.log(`Found element ${key} with value: ${value}`);
                            results[key] = value !== '';
                        }
                    });
                    
                    const allPresent = Object.values(results).every(v => v);
                    console.log('All elements present and populated:', allPresent);
                    return allPresent;
                }
                checkElements();
                """
                if run_javascript_browser(js_check):
                    logger.info("Page reload successful, all elements present")
                    break
                
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"Page not fully loaded, retry {retry_count}/{max_retries}")
                    time.sleep(3)  # Wait before retry
                else:
                    raise Exception("Failed to verify page load after reload")
            except Exception as e:
                logger.error(f"Error verifying page load: {str(e)}")
                if retry_count >= max_retries:
                    raise
                retry_count += 1
                time.sleep(3)
        
        # Check if token is expired
        if is_token_expired():
            logging.info("Token expired, attempting to refresh")
            if not handle_token_expiration():
                raise Exception("Failed to refresh token")
        
        # Extract data with retry logic
        logger.info("Extracting metrics after reload")
        extract_script = """
        (async function() {
            try {
                const elements = {
                    '线上销售额元': document.querySelector('p[devinid="54"]'),
                    '线下销售额元': document.querySelector('p[devinid="59"]'),
                    '结算金额元': document.querySelector('p[devinid="64"]'),
                    '新增会员人': document.querySelector('p[devinid="69"]'),
                    '新增潜客人': document.querySelector('p[devinid="74"]'),
                    '售课节': document.querySelector('p[devinid="79"]'),
                    '客流人次': document.querySelector('p[devinid="84"]')
                };
                
                const missingElements = Object.entries(elements)
                    .filter(([key, el]) => !el)
                    .map(([key]) => key);
                
                if (missingElements.length > 0) {
                    console.error('Missing elements:', missingElements.join(', '));
                    return null;
                }
                
                const metrics = {};
                Object.entries(elements).forEach(([key, el]) => {
                    metrics[key] = el.textContent;
                });
                
                console.log('EXTRACTED_METRICS:', JSON.stringify(metrics));
                return metrics;
            } catch (error) {
                console.error('Error extracting metrics:', error);
                return null;
            }
        })();
        """
        
        # Try to extract data with retries
        max_retries = 3
        retry_delay = 2
        metrics = None
        
        for attempt in range(max_retries):
            run_javascript_browser(extract_script)
            console_output = get_browser_console()
            
            # Parse metrics from console output
            for line in console_output.split('\n'):
                if 'EXTRACTED_METRICS:' in line:
                    try:
                        metrics_json = line.split('EXTRACTED_METRICS:', 1)[1].strip()
                        raw_metrics = json.loads(metrics_json)
                        if raw_metrics:
                            metrics = raw_metrics
                            logger.info(f"Successfully extracted metrics on attempt {attempt + 1}")
                            break
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse metrics JSON: {e}")
                    except Exception as e:
                        logger.error(f"Error processing metrics: {e}")
            
            if metrics:
                break
                
            if attempt < max_retries - 1:
                logger.warning(f"Retry {attempt + 1}/{max_retries} - waiting {retry_delay}s")
                time.sleep(retry_delay)
        
        if not metrics:
            raise Exception("Failed to extract metrics after retries")
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
