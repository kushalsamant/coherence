/**
 * Client-Side Configuration
 * Safe to use in client components
 */

// Get API URL for client-side usage
export const getApiUrl = () => {
  if (typeof window === 'undefined') {
    // Server-side
    return process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';
  }
  // Client-side - only use NEXT_PUBLIC variables
  return process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';
};

export const CLIENT_CONFIG = {
  API_URL: getApiUrl(),
};

