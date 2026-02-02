/**
 * Simplified recording script with better error handling and output
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DEMO_URL = 'http://localhost:3000/sketch2bim/demo';
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'demo-videos');

async function recordDemo() {
  console.log('='.repeat(60));
  console.log('🎬 Sketch2BIM Demo Video Recorder');
  console.log('='.repeat(60));
  
  // Create output directory
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    console.log('✅ Created output directory:', OUTPUT_DIR);
  }

  console.log('🚀 Launching browser...');
  const browser = await chromium.launch({
    headless: false,
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
    
    console.log('📄 Navigating to:', DEMO_URL);
    try {
      await page.goto(DEMO_URL, { waitUntil: 'networkidle2', timeout: 30000 });
      console.log('✅ Page loaded successfully');
    } catch (error) {
      console.error('❌ Failed to load page:', error.message);
      console.log('💡 Make sure dev server is running: npm run dev');
      throw error;
    }
    
    await page.waitForTimeout(2000);

    console.log('🎬 Video recording started');
    console.log('⏳ Waiting 2 seconds...');
    await page.waitForTimeout(2000);

    // Click start processing
    console.log('🖱️  Looking for "Start Processing" button...');
    try {
      const startButton = await page.locator('button:has-text("Start Processing")').first();
      await startButton.waitFor({ timeout: 5000 });
      await startButton.click();
      console.log('✅ Button clicked');
    } catch (error) {
      console.error('❌ Could not find or click button:', error.message);
      // Try alternative selector
      try {
        await page.click('button');
        console.log('✅ Clicked button (alternative method)');
      } catch (e) {
        throw error;
      }
    }
    
    console.log('⏳ Recording processing animation (6 seconds)...');
    await page.waitForTimeout(6000);

    console.log('⏳ Recording completed state (3 seconds)...');
    await page.waitForTimeout(3000);

    console.log('📜 Scrolling to show all features...');
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(2000);

    console.log('✅ Recording complete! Finalizing video...');
    
    // Close context to finalize video
    await context.close();
    await browser.close();

    // Wait a moment for file to be written
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Find the recorded video file
    const files = fs.readdirSync(OUTPUT_DIR);
    console.log('📁 Files in output directory:', files);
    
    const videoFile = files.find(f => f.endsWith('.webm'));
    
    if (videoFile) {
      const videoPath = path.join(OUTPUT_DIR, videoFile);
      const finalPath = path.join(OUTPUT_DIR, 'sketch2bim-demo.webm');
      
      // Rename to final name
      if (videoPath !== finalPath) {
        fs.renameSync(videoPath, finalPath);
      }
      
      const stats = fs.statSync(finalPath);
      const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);
      
      console.log('\n' + '='.repeat(60));
      console.log('✅ VIDEO RECORDED SUCCESSFULLY!');
      console.log('='.repeat(60));
      console.log(`📁 Location: ${finalPath}`);
      console.log(`📊 File size: ${fileSizeMB} MB`);
      console.log('\n💡 Next steps:');
      console.log('   1. Review the video');
      console.log('   2. Convert to MP4 if needed:');
      console.log(`      ffmpeg -i "${finalPath}" -c:v libx264 -c:a aac "${OUTPUT_DIR}/sketch2bim-demo.mp4"`);
      console.log('   3. Or use online converter: https://convertio.co/webm-mp4/');
      console.log('   4. Add narration, captions, or transitions');
      console.log('   5. Upload to YouTube');
      console.log('   6. Update landing page with video ID');
      console.log('='.repeat(60));
    } else {
      console.log('\n⚠️  Video file not found in:', OUTPUT_DIR);
      console.log('📁 Available files:', files);
    }

  } catch (error) {
    console.error('\n❌ ERROR:', error.message);
    console.error(error.stack);
    console.log('\n💡 Troubleshooting:');
    console.log('   1. Make sure dev server is running: npm run dev');
    console.log('   2. Check that demo page exists: http://localhost:3000/sketch2bim/demo');
    console.log('   3. Verify Playwright is installed: npm install playwright');
    console.log('   4. Verify Chromium is installed: npx playwright install chromium');
  } finally {
    try {
      await browser.close();
    } catch (e) {
      // Ignore
    }
  }
}

// Run the recording
if (require.main === module) {
  recordDemo().catch(error => {
    console.error('Fatal error:', error);
    console.error(error.stack);
    process.exit(1);
  });
}
