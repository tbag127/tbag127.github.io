import time
from browser_automation import navigate_browser, run_javascript_browser, view_browser, reload_and_verify_page

def test_browser_automation():
    """Test the browser automation functions"""
    print("=== Testing Browser Automation ===")
    
    # Test navigation
    print("\nTesting navigation:")
    navigate_browser('https://www.iwod.cn/admin/dataAnalysis/storeSummary?title=%E6%95%B0%E6%8D%AE%E6%A6%82%E5%86%B5')
    
    # Test page reload and verification
    print("\nTesting page reload and verification:")
    expected_values = {'客流': 3, '售课': 4}  # Current expected values
    if reload_and_verify_page(max_retries=3, expected_values=expected_values):
        print("✓ Page reload successful - values verified")
    else:
        print("✗ Page reload failed or values don't match expected")
        
    # Test data extraction
    print("\nTesting data extraction:")
    js_script = """
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
        
        const metrics = {};
        Object.entries(elements).forEach(([key, el]) => {
            if (!el) {
                console.error(`Missing element: ${key}`);
                return;
            }
            metrics[key] = el.textContent.trim();
            console.log(`${key}: ${metrics[key]}`);
        });
        
        console.log('EXTRACTED_METRICS:', JSON.stringify(metrics, null, 2));
    } catch (error) {
        console.error('Error extracting metrics:', error);
    }
    """
    run_javascript_browser(js_script)
    
    # Test browser view
    print("\nTesting browser view:")
    view_browser()
    
    print("\n=== Browser Automation Tests Complete ===")


if __name__ == "__main__":
    test_browser_automation()
