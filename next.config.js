/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // Preserve existing Jekyll structure during migration
  // We'll migrate content files gradually
}

module.exports = nextConfig
