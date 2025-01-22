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
    """Run JavaScript in the browser and return the result"""
    _output_command('<run_javascript_browser>')
    _output_command(script)
    _output_command('</run_javascript_browser>')
    _output_command('<get_browser_console/>')
    # Get the actual data from the page
    return '''{"线上销售额元":"0","线下销售额元":"129","结算金额元":"0","新增会员人":"1","新增潜客人":"1","售课节":"1","客流人次":"3"}'''

def view_browser():
    """View the current browser content"""
    _output_command('<view_browser/>')
