// Note: Environment variables are loaded from root .env.local for local development
// Production environment variables are configured in Vercel dashboard

const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'output: export' to enable API routes for centralized authentication
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // Transpile workspace packages for monorepo support
  transpilePackages: ['@kushalsamant/design-template', '@kvshvl/shared-frontend'],
  // Skip prerendering for pages with dynamic data (auth, subscriptions)
  skipTrailingSlashRedirect: false,
  experimental: {
    // Disable static optimization for pages using auth
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}

module.exports = nextConfig
