/**
 * Centralized Configuration
 * Single source of truth for environment-dependent values
 */

// API URLs
export const API_CONFIG = {
  PLATFORM_API_URL: process.env.NEXT_PUBLIC_PLATFORM_API_URL || 
                    (process.env.NODE_ENV === 'production' 
                      ? 'https://platform-api.onrender.com' 
                      : 'http://localhost:8000'),
  
  FRONTEND_URL: process.env.NEXTAUTH_URL || 
                (process.env.NODE_ENV === 'production'
                  ? 'https://kvshvl.in'
                  : 'http://localhost:3000'),
};

// Auth Configuration
export const AUTH_CONFIG = {
  BASE_URL: process.env.REFRAME_AUTH_URL || 
            process.env.AUTH_URL || 
            process.env.REFRAME_NEXT_PUBLIC_SITE_URL || 
            process.env.NEXT_PUBLIC_SITE_URL || 
            API_CONFIG.FRONTEND_URL,
};

// Rate Limit Configuration
export const RATE_LIMIT_CONFIG = {
  STANDARD: {
    requests: 10,
    window: '10 s',
  },
  STRICT: {
    requests: 3,
    window: '1 m',
  },
  AUTH: {
    requests: 5,
    window: '1 m',
  },
};

