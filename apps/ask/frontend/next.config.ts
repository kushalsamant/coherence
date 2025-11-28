import type { NextConfig } from "next";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";

const appEnvPath = path.resolve(process.cwd(), "../../ask.env.production");
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
}

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/static/images/**',
      },
      {
        protocol: 'https',
        hostname: 'ask.kvshvl.in',
        pathname: '/static/images/**',
      },
    ],
  },
};

export default nextConfig;
