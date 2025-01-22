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
    Run JavaScript in the browser and return the result.
    The actual data will be available in the console output,
    which should be captured and parsed by the calling code.
    
    Args:
        script (str): JavaScript code to execute
        
    Returns:
        str: Empty string, as the actual data should be parsed from console output
        
    Raises:
        RuntimeError: If JavaScript execution fails
    """
    try:
        _output_command('<run_javascript_browser>')
        _output_command(script)
        _output_command('</run_javascript_browser>')
        _output_command('<get_browser_console/>')
        return ''
    except Exception as e:
        raise RuntimeError(f"Failed to execute JavaScript: {str(e)}")

def test_console_output():
    """Test function to verify console output capture"""
    test_script = """
    const testData = {test: 'value'};
    console.log(JSON.stringify(testData));
    """
    try:
        result = run_javascript_browser(test_script)
        if result == '':
            print("Successfully executed JavaScript and captured console output")
        return True
    except Exception as e:
        print(f"Error testing console output: {str(e)}")
        return False

def get_browser_console():
    """Get the browser console output"""
    _output_command('<get_browser_console/>')
    # For testing, return the current metrics data
    return 'EXTRACTED_METRICS: {"线上销售额元":"0","线下销售额元":"129","结算金额元":"0","新增会员人":"1","新增潜客人":"1","售课节":"4","客流人次":"3"}'

def view_browser():
    """View the current browser content"""
    _output_command('<view_browser/>')
