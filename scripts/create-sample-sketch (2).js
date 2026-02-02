/**
 * Script to create a simple sample architectural sketch
 * Run with: node scripts/create-sample-sketch.js
 * 
 * Requires: canvas package (npm install canvas)
 * Or use an online tool to create the sketch manually
 */

const fs = require('fs');
const path = require('path');

// Simple SVG-based sample sketch (no dependencies)
const sampleSketchSVG = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="900" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="1200" height="900" fill="#ffffff"/>
  
  <!-- Title -->
  <text x="600" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#000000">
    Sample Architectural Floor Plan
  </text>
  
  <!-- Scale indicator -->
  <text x="50" y="80" font-family="Arial, sans-serif" font-size="16" fill="#333333">
    Scale: 1:100
  </text>
  
  <!-- Outer walls -->
  <rect x="200" y="150" width="800" height="600" fill="none" stroke="#000000" stroke-width="4"/>
  
  <!-- Room 1 (Top Left) -->
  <rect x="220" y="170" width="360" height="260" fill="none" stroke="#000000" stroke-width="2"/>
  <text x="400" y="300" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="#000000">Bedroom</text>
  
  <!-- Door 1 -->
  <line x1="400" y1="430" x2="400" y2="450" stroke="#000000" stroke-width="3"/>
  <path d="M 380 430 A 20 20 0 0 1 400 450" fill="none" stroke="#000000" stroke-width="2"/>
  
  <!-- Room 2 (Top Right) -->
  <rect x="620" y="170" width="360" height="260" fill="none" stroke="#000000" stroke-width="2"/>
  <text x="800" y="300" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="#000000">Kitchen</text>
  
  <!-- Window 1 -->
  <rect x="220" y="160" width="80" height="10" fill="#87CEEB" stroke="#000000" stroke-width="2"/>
  
  <!-- Window 2 -->
  <rect x="900" y="300" width="10" height="80" fill="#87CEEB" stroke="#000000" stroke-width="2"/>
  
  <!-- Living Room (Bottom) -->
  <rect x="220" y="470" width="760" height="260" fill="none" stroke="#000000" stroke-width="2"/>
  <text x="600" y="600" font-family="Arial, sans-serif" font-size="20" text-anchor="middle" fill="#000000">Living Room</text>
  
  <!-- Door 2 -->
  <line x1="620" y1="470" x2="640" y2="470" stroke="#000000" stroke-width="3"/>
  <path d="M 620 450 A 20 20 0 0 1 640 470" fill="none" stroke="#000000" stroke-width="2"/>
  
  <!-- Window 3 -->
  <rect x="500" y="720" width="200" height="10" fill="#87CEEB" stroke="#000000" stroke-width="2"/>
  
  <!-- Dimensions (optional) -->
  <line x1="200" y1="800" x2="1000" y2="800" stroke="#666666" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="600" y="820" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#666666">8.0 m</text>
</svg>`;

// Save SVG file
const publicDir = path.join(__dirname, '..', 'public');
const svgPath = path.join(publicDir, 'sample-sketch.svg');

if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

fs.writeFileSync(svgPath, sampleSketchSVG);
console.log('✅ Created sample-sketch.svg at:', svgPath);
console.log('');
console.log('📝 Next steps:');
console.log('1. Convert SVG to PNG (use online converter or ImageMagick)');
console.log('2. Or use the SVG directly by updating UploadForm.tsx');
console.log('3. Recommended: Create a hand-drawn sketch for better demo');
console.log('');
console.log('💡 Tip: Use a tool like:');
console.log('   - https://convertio.co/svg-png/');
console.log('   - ImageMagick: convert sample-sketch.svg sample-sketch.png');
console.log('   - Or create manually in any drawing app');
