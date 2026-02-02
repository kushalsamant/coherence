/**
 * Automated Video Recording Script for Demo Page
 * 
 * This script uses Playwright to automatically record the demo page as a video
 * 
 * Requirements:
 *   npm install playwright
 *   npx playwright install chromium
 * 
 * Usage:
 *   1. Start your dev server: npm run dev
 *   2. Run this script: node scripts/record-demo-video.js
 *   3. Video will be saved to public/demo-video.webm
 *   4. Convert to MP4 if needed (use ffmpeg or online converter)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DEMO_URL = 'http://localhost:3000/sketch2bim/demo';
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'demo-videos');

async function recordDemo() {
  // Create output directory
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  console.log('🚀 Launching browser...');
  console.log('📋 Output directory:', OUTPUT_DIR);
  console.log('🌐 Demo URL:', DEMO_URL);
  const browser = await chromium.launch({
    headless: false, // Set to true for headless recording
  });

  try {
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      recordVideo: {
        dir: OUTPUT_DIR,
        size: { width: 1920, height: 1080 }
      }
    });

    const page = await context.newPage();
    
    console.log('📄 Navigating to demo page...');
    await page.goto(DEMO_URL, { waitUntil: 'networkidle2' });
    await page.waitForTimeout(2000); // Wait for page to fully load

    console.log('🎬 Starting video recording...');
    console.log('⏳ Waiting 2 seconds before starting interaction...');
    await page.waitForTimeout(2000);

    // Click start processing
    console.log('🖱️  Clicking "Start Processing"...');
    const startButton = await page.locator('button:has-text("Start Processing"), button:has-text("Start Processing →")').first();
    await startButton.click();
    
    console.log('⏳ Recording processing animation (6 seconds)...');
    await page.waitForTimeout(6000); // Wait for processing to complete

    console.log('⏳ Recording completed state (3 seconds)...');
    await page.waitForTimeout(3000);

    // Scroll to show download options and 3D viewer
    console.log('📜 Scrolling to show all features...');
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(2000);

    console.log('✅ Recording complete! Closing browser...');
    
    // Close context to finalize video
    await context.close();
    await browser.close();

    // Find the recorded video file
    const files = fs.readdirSync(OUTPUT_DIR);
    const videoFile = files.find(f => f.endsWith('.webm'));
    
    if (videoFile) {
      const videoPath = path.join(OUTPUT_DIR, videoFile);
      const finalPath = path.join(OUTPUT_DIR, 'sketch2bim-demo.webm');
      
      // Rename to final name
      if (videoPath !== finalPath) {
        fs.renameSync(videoPath, finalPath);
      }
      
      console.log('\n✅ Video recorded successfully!');
      console.log(`📁 Location: ${finalPath}`);
      console.log('\n💡 Next steps:');
      console.log('   1. Review the video');
      console.log('   2. Convert to MP4 if needed:');
      console.log('      ffmpeg -i public/demo-videos/sketch2bim-demo.webm -c:v libx264 -c:a aac public/demo-videos/sketch2bim-demo.mp4');
      console.log('   3. Or use online converter: https://convertio.co/webm-mp4/');
      console.log('   4. Add narration, captions, or transitions in video editor');
      console.log('   5. Upload to YouTube');
      console.log('   6. Update landing page with video ID');
    } else {
      console.log('⚠️  Video file not found. Check', OUTPUT_DIR);
    }

  } catch (error) {
    console.error('❌ Error:', error);
    console.log('\n💡 Make sure:');
    console.log('   1. Your dev server is running (npm run dev)');
    console.log('   2. The demo page is accessible at', DEMO_URL);
    console.log('   3. Playwright is installed: npm install playwright');
    console.log('   4. Chromium is installed: npx playwright install chromium');
  } finally {
    await browser.close();
  }
}

// Run the recording
recordDemo().catch(console.error);
