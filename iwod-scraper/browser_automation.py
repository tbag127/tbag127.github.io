"""Browser automation wrapper functions for the Devin environment"""
import time
import sys
import os

def _output_command(command):
    """Helper function to output Devin commands properly"""
    sys.stdout.write(command + '\n')
    sys.stdout.flush()
    time.sleep(1)  # Give command time to execute

def navigate_browser(url):
    """Navigate to a URL in the browser"""
    _output_command(f'<navigate_browser url="{url}"/>')
    time.sleep(5)  # Wait for page load

def run_javascript_browser(script):
    """
    Run JavaScript in the browser and return the console output
    
    Args:
        script (str): JavaScript code to execute
        
    Returns:
        str: Console output from the JavaScript execution
    """
    _output_command('<run_javascript_browser>')
    _output_command(script)
    _output_command('</run_javascript_browser>')
    return get_browser_console()

def reload_and_verify_page(max_retries=3, expected_values=None):
    """
    Reload the page and verify elements are present with their values
    
    Args:
        max_retries (int): Maximum number of retry attempts
        expected_values (dict, optional): Expected values to verify against, e.g. {'客流': 3, '售课': 4}
        
    Returns:
        bool: True if page reloaded successfully with valid data, False otherwise
    """
    for attempt in range(max_retries):
        # Force a hard reload
        run_javascript_browser('window.location.reload(true);')
        time.sleep(5)  # Initial wait for reload
        
        # View the page content to verify load
        _output_command('<view_browser/>')
        
        # Check for elements and verify their values
        verify_script = """
        try {
            const requiredElements = {
                '客流': document.querySelector('p[devinid="84"]'),
                '售课': document.querySelector('p[devinid="79"]')
            };
            
            const results = {};
            let allValid = true;
            
            Object.entries(requiredElements).forEach(([key, el]) => {
                if (!el || !el.textContent) {
                    console.error(`Missing element: ${key}`);
                    allValid = false;
                    return;
                }
                
                const value = el.textContent.trim();
                const numValue = parseInt(value, 10);
                
                if (isNaN(numValue)) {
                    console.error(`Invalid value for ${key}: ${value}`);
                    allValid = false;
                    return;
                }
                
                results[key] = numValue;
                console.log(`Found ${key}: ${numValue}`);
            });
            
            if (allValid) {
                // Check against expected values if provided
                const expectedValues = {expected_values};
                if (expectedValues) {
                    Object.entries(expectedValues).forEach(([key, expected]) => {
                        if (results[key] !== expected) {
                            console.error(`Value mismatch for ${key}: expected ${expected}, got ${results[key]}`);
                            allValid = false;
                        }
                    });
                }
                
                if (allValid) {
                    console.log('VERIFY_RESULT: success');
                    console.log('ELEMENT_VALUES:', JSON.stringify(results));
                } else {
                    console.log('VERIFY_RESULT: failed');
                }
            } else {
                console.log('VERIFY_RESULT: failed');
            }
            
            return allValid;
        } catch (e) {
            console.error('Error verifying page:', e);
            return false;
        }
        """
        
        console_output = run_javascript_browser(verify_script) or ''
        
        # Parse verification result and values
        if console_output and 'VERIFY_RESULT: success' in console_output:
            return True
            
        if attempt < max_retries - 1:
            print(f"Page verification failed, retrying ({attempt + 1}/{max_retries})")
            time.sleep(3)  # Wait before retry
            
    return False  # All retries failed

def get_browser_console():
    """
    Get the browser console output
    
    Returns:
        str: Console output from browser, empty string if no output
    """
    _output_command('<get_browser_console/>')
    return ''  # The actual console output will be captured by Devin's environment

def view_browser():
    """View the current browser content"""
    _output_command('<view_browser/>')
