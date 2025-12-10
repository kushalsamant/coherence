// Quick test to verify Playwright is working
const { chromium } = require('playwright');

(async () => {
  console.log('Testing Playwright...');
  try {
    const browser = await chromium.launch({ headless: true });
    console.log('✅ Browser launched successfully');
    const page = await browser.newPage();
    await page.goto('https://example.com');
    console.log('✅ Page navigation works');
    await browser.close();
    console.log('✅ Playwright is working correctly!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
