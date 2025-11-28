const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

const appEnvPath = path.resolve(__dirname, '../../sketch2bim.env.production');
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    domains: ['kvshvl.b-cdn.net'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.SKETCH2BIM_NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  webpack: (config) => {
    // Handle web-ifc WebAssembly
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };
    return config;
  },
};

module.exports = nextConfig;

