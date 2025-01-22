import time
from browser_automation import navigate_browser, run_javascript_browser, view_browser

def test_browser_automation():
    """Test the browser automation functions"""
    print("Testing browser automation...")
    
    # Test navigation
    print("\nTesting navigation:")
    navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
    
    # Test JavaScript execution
    print("\nTesting JavaScript execution:")
    js_script = """
    const metrics = {};
    document.querySelectorAll('div[type="flex"] > a').forEach(card => {
        const title = card.querySelector('p:first-child').textContent.replace(/[()（）]/g, '');
        const value = card.querySelector('p:nth-child(2)').textContent;
        metrics[title] = value;
    });
    return JSON.stringify(metrics);
    """
    result = run_javascript_browser(js_script)
    print(f"JavaScript result: {result}")
    
    # Test browser view
    print("\nTesting browser view:")
    view_browser()

if __name__ == "__main__":
    test_browser_automation()
