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
  
  FRONTEND_URL: process.env.NEXT_PUBLIC_SITE_URL || 
                process.env.PLATFORM_FRONTEND_URL ||
                (process.env.NODE_ENV === 'production'
                  ? 'https://kvshvl.in'
                  : 'http://localhost:3000'),
};

// Auth Configuration
export const AUTH_CONFIG = {
  BASE_URL: process.env.AUTH_URL || 
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

// Currency Conversion Configuration
// INR to USD conversion rate (configurable via environment variable)
// Default: 0.0118 (₹1 ≈ $0.0118, based on ~₹84.68 per $1 USD as of Dec 2024)
// Should be updated regularly via NEXT_PUBLIC_INR_TO_USD_RATE environment variable to reflect current exchange rates
export const CURRENCY_CONFIG = {
  INR_TO_USD: parseFloat(process.env.NEXT_PUBLIC_INR_TO_USD_RATE || '0.0118'),
};

