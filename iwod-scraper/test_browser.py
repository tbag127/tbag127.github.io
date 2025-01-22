import time
from browser_automation import navigate_browser, run_javascript_browser, view_browser, test_console_output

def test_browser_automation():
    """Test the browser automation functions"""
    print("=== Testing Browser Automation ===")
    
    # Test navigation
    print("\nTesting navigation:")
    navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
    
    # Test JavaScript execution and console output
    print("\nTesting JavaScript execution and console output:")
    js_script = """
    try {
        const metrics = {};
        const elements = document.querySelectorAll('div[type="flex"] > a');
        if (!elements || elements.length === 0) {
            console.error('No metric elements found on page');
            return;
        }
        elements.forEach(card => {
            const titleEl = card.querySelector('p:first-child');
            const valueEl = card.querySelector('p:nth-child(2)');
            if (titleEl && valueEl) {
                const title = titleEl.textContent.replace(/[()（）]/g, '');
                const value = valueEl.textContent;
                metrics[title] = value;
            }
        });
        console.log('METRICS_DATA:', JSON.stringify(metrics, null, 2));
    } catch (error) {
        console.error('Error extracting metrics:', error);
    }
    """
    result = run_javascript_browser(js_script)
    if result == '':
        print("JavaScript execution completed - check console output for 'METRICS_DATA:'")
    else:
        print("Warning: Expected empty string result, got:", result)
    
    # Test console output specifically
    print("\nTesting console output capture:")
    if test_console_output():
        print("Console output test passed")
    else:
        print("Console output test failed")
    
    # Test browser view
    print("\nTesting browser view:")
    view_browser()
    
    print("\n=== Browser Automation Tests Complete ===")


if __name__ == "__main__":
    test_browser_automation()
