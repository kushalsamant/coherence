#!/usr/bin/env node
/**
 * Script to split .env files into frontend and backend versions
 * 
 * Usage:
 *   node scripts/split-env-files.js [.env.local|.env.production]
 * 
 * This script reads a .env file and splits it into:
 *   - .env.{name}.frontend (NEXT_PUBLIC_* variables)
 *   - .env.{name}.backend (PLATFORM_* and other server-side variables)
 */

const fs = require('fs');
const path = require('path');

function splitEnvFile(envFilePath) {
  const envFile = path.resolve(envFilePath);
  
  if (!fs.existsSync(envFile)) {
    console.error(`Error: File ${envFile} does not exist`);
    process.exit(1);
  }

  const content = fs.readFileSync(envFile, 'utf-8');
  const lines = content.split('\n');
  
  const frontendVars = [];
  const backendVars = [];
  const comments = [];
  let currentSection = null;
  
  // Determine the base name (e.g., ".env.local" -> "local", ".env.production" -> "production")
  const basename = path.basename(envFile);
  const match = basename.match(/^\.env\.?(.+)?$/);
  const suffix = match && match[1] ? match[1] : '';
  const newSuffix = suffix ? `.${suffix}` : '';
  
  frontendVars.push(`# Frontend Environment Variables (${suffix || 'default'})`);
  frontendVars.push(`# Generated from ${basename}`);
  frontendVars.push(`# These variables are exposed to the browser (NEXT_PUBLIC_* prefix)`);
  frontendVars.push('');
  
  backendVars.push(`# Backend Environment Variables (${suffix || 'default'})`);
  backendVars.push(`# Generated from ${basename}`);
  backendVars.push(`# These variables are server-side only (PLATFORM_* and other prefixes)`);
  backendVars.push('');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    // Skip empty lines (we'll add them back)
    if (line === '') {
      if (currentSection === 'frontend') {
        frontendVars.push('');
      } else if (currentSection === 'backend') {
        backendVars.push('');
      } else {
        // Preserve empty lines in both files if they're between sections
        frontendVars.push('');
        backendVars.push('');
      }
      continue;
    }
    
    // Preserve comments
    if (line.startsWith('#')) {
      // Check if it's a section header
      if (line.includes('===') || line.includes('FRONTEND') || line.includes('NEXT_PUBLIC')) {
        frontendVars.push(line);
        currentSection = 'frontend';
      } else if (line.includes('BACKEND') || line.includes('PLATFORM_') || line.includes('DATABASE') || line.includes('RAZORPAY') || line.includes('AUTH') || line.includes('SECRET')) {
        backendVars.push(line);
        currentSection = 'backend';
      } else {
        // Generic comment - add to both
        frontendVars.push(line);
        backendVars.push(line);
      }
      continue;
    }
    
    // Parse variable
    const match = line.match(/^([^=]+)=(.*)$/);
    if (!match) {
      // Not a valid env line, preserve as comment
      frontendVars.push(line);
      backendVars.push(line);
      continue;
    }
    
    const key = match[1].trim();
    const value = match[2].trim();
    
    // Categorize variable
    if (key.startsWith('NEXT_PUBLIC_')) {
      frontendVars.push(`${key}=${value}`);
      currentSection = 'frontend';
    } else if (key.startsWith('PLATFORM_') || 
               key.startsWith('SKETCH2BIM_') ||
               key.includes('SECRET') ||
               key.includes('DATABASE') ||
               key.includes('RAZORPAY') ||
               key.includes('SUPABASE_SERVICE') ||
               key.includes('AUTH') ||
               key.includes('ADMIN') ||
               key.includes('CORS') ||
               key.includes('REDIS') ||
               key.includes('BUNNY') ||
               key.includes('GROQ') ||
               key.includes('OPENAI') ||
               key === 'NODE_ENV' ||
               key.startsWith('RENDER_')) {
      backendVars.push(`${key}=${value}`);
      currentSection = 'backend';
    } else {
      // Unknown variable - ask user or add to backend by default (safer)
      // For now, add to backend as it's safer to not expose unknown vars
      backendVars.push(`${key}=${value}`);
      currentSection = 'backend';
    }
  }
  
  // Write frontend file
  const frontendFile = path.resolve(path.dirname(envFile), `.env${newSuffix}.frontend`);
  fs.writeFileSync(frontendFile, frontendVars.join('\n') + '\n');
  console.log(`✅ Created ${path.basename(frontendFile)}`);
  
  // Write backend file
  const backendFile = path.resolve(path.dirname(envFile), `.env${newSuffix}.backend`);
  fs.writeFileSync(backendFile, backendVars.join('\n') + '\n');
  console.log(`✅ Created ${path.basename(backendFile)}`);
  
  console.log(`\n📝 Note: Original file ${basename} has been preserved.`);
  console.log(`   You can delete it after verifying the split files work correctly.`);
}

// Main execution
const envFile = process.argv[2];

if (!envFile) {
  console.log('Usage: node scripts/split-env-files.js [.env.local|.env.production]');
  console.log('');
  console.log('This script splits a .env file into:');
  console.log('  - .env.{name}.frontend (NEXT_PUBLIC_* variables)');
  console.log('  - .env.{name}.backend (PLATFORM_* and other server-side variables)');
  process.exit(1);
}

splitEnvFile(envFile);

