// Load shared .env.production from this repo's root (since this is where it lives)
// This file is the source of truth for production environment variables
try {
  const dotenv = require('dotenv');
  const fs = require('fs');
  const path = require('path');
  const sharedEnvPath = path.resolve(__dirname, '.env.production');
  if (fs.existsSync(sharedEnvPath)) {
    dotenv.config({ path: sharedEnvPath, override: false });
  }
} catch (e) {
  // dotenv not installed, skip (optional for static sites)
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'output: export' to enable API routes for centralized authentication
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
