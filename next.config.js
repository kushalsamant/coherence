// Note: Environment variables are loaded from root .env.local for local development
// Production environment variables are configured in Vercel dashboard

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'output: export' to enable API routes for centralized authentication
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
