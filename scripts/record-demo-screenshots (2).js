/**
 * Script to capture screenshots of the demo page for video creation
 * 
 * Requirements:
 *   npm install puppeteer
 * 
 * Usage:
 *   1. Start your dev server: npm run dev
 *   2. Run this script: node scripts/record-demo-screenshots.js
 *   3. Screenshots will be saved to public/demo-screenshots/
 *   4. Use these screenshots or screen recording software to create your video
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(__dirname, '..', 'public', 'demo-screenshots');
const DEMO_URL = 'http://localhost:3000/sketch2bim/demo';

async function captureDemo() {
  // Create screenshot directory
  if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  }

  console.log('🚀 Starting browser...');
  const browser = await puppeteer.launch({
    headless: false, // Set to true if you don't want to see the browser
    defaultViewport: { width: 1920, height: 1080 }
  });

  try {
    const page = await browser.newPage();
    
    console.log('📄 Navigating to demo page...');
    await page.goto(DEMO_URL, { waitUntil: 'networkidle2' });
    await page.waitForTimeout(2000); // Wait for page to fully load

    // Screenshot 1: Initial state (upload ready)
    console.log('📸 Capturing screenshot 1: Initial upload state...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, '01-initial-upload.png'),
      fullPage: true
    });

    // Click start processing
    console.log('🖱️  Clicking "Start Processing"...');
    await page.click('button:has-text("Start Processing")');
    await page.waitForTimeout(500);

    // Screenshot 2: Processing started
    console.log('📸 Capturing screenshot 2: Processing started...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, '02-processing-started.png'),
      fullPage: true
    });

    // Wait and capture progress at different stages
    const progressStages = [25, 50, 75, 95];
    for (let i = 0; i < progressStages.length; i++) {
      const targetProgress = progressStages[i];
      console.log(`⏳ Waiting for ${targetProgress}% progress...`);
      
      // Wait for progress to reach target (with timeout)
      await page.waitForFunction(
        (target) => {
          const progressText = document.querySelector('#progressText, [class*="progress"]');
          if (!progressText) return false;
          const currentProgress = parseInt(progressText.textContent) || 0;
          return currentProgress >= target;
        },
        { timeout: 10000 },
        targetProgress
      ).catch(() => {
        console.log(`⚠️  Progress ${targetProgress}% not reached, continuing...`);
      });

      await page.waitForTimeout(500);
      console.log(`📸 Capturing screenshot ${3 + i}: ${targetProgress}% progress...`);
      await page.screenshot({
        path: path.join(SCREENSHOT_DIR, `0${3 + i}-progress-${targetProgress}.png`),
        fullPage: true
      });
    }

    // Wait for completion
    console.log('⏳ Waiting for completion...');
    await page.waitForSelector('[class*="completed"], [id*="completed"]', { timeout: 15000 })
      .catch(() => console.log('⚠️  Completion indicator not found, continuing...'));
    
    await page.waitForTimeout(1000);

    // Screenshot 7: Completed state
    console.log('📸 Capturing screenshot 7: Completed state...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, '07-completed.png'),
      fullPage: true
    });

    // Screenshot 8: Download options visible
    console.log('📸 Capturing screenshot 8: Download options...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, '08-download-options.png'),
      fullPage: true
    });

    // Scroll to 3D viewer if needed
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(500);

    // Screenshot 9: 3D viewer
    console.log('📸 Capturing screenshot 9: 3D viewer...');
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, '09-3d-viewer.png'),
      fullPage: true
    });

    console.log('\n✅ Screenshots captured successfully!');
    console.log(`📁 Location: ${SCREENSHOT_DIR}`);
    console.log('\n💡 Next steps:');
    console.log('   1. Review the screenshots');
    console.log('   2. Use screen recording software to record the demo page');
    console.log('   3. Or use the screenshots in a video editor');
    console.log('   4. Add narration and captions');

  } catch (error) {
    console.error('❌ Error:', error);
    console.log('\n💡 Make sure:');
    console.log('   1. Your dev server is running (npm run dev)');
    console.log('   2. The demo page is accessible at', DEMO_URL);
  } finally {
    await browser.close();
  }
}

// Run the capture
captureDemo().catch(console.error);
