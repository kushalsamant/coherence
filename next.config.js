// Note: Environment variables are now loaded from app-specific files:
// - ask.env.production
// - reframe.env.production
// - sketch2bim.env.production
// Each app loads its own file in its next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'output: export' to enable API routes for centralized authentication
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
