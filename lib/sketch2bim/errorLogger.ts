'use client';

type ErrorContext = Record<string, unknown> | undefined;

const isProduction = process.env.NODE_ENV === 'production';

const API_BASE = process.env.SKETCH2BIM_NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_URL;

// Strip sensitive data from error objects
function sanitizeError(error: any): any {
  if (!error) return error;
  
  // Create a sanitized copy
  const sanitized: any = {};
  
  // Only include safe fields
  if (error.message) sanitized.message = error.message;
  if (error.name) sanitized.name = error.name;
  if (error.code) sanitized.code = error.code;
  if (error.status) sanitized.status = error.status;
  
  // Strip sensitive fields
  const sensitiveFields = [
    'response', 'data', 'detail', 'stack', 'config', 'request',
    'apiKey', 'token', 'password', 'secret', 'key', 'authorization'
  ];
  
  // Sanitize context
  if (error.response) {
    sanitized.response = {
      status: error.response.status,
      statusText: error.response.statusText,
    };
  }
  
  return sanitized;
}

// Strip sensitive data from context
function sanitizeContext(context?: ErrorContext): ErrorContext {
  if (!context) return context;
  
  const sanitized: Record<string, unknown> = {};
  const sensitiveKeys = ['apiKey', 'token', 'password', 'secret', 'key', 'authorization', 'accessToken'];
  
  for (const [key, value] of Object.entries(context)) {
    if (sensitiveKeys.some(sk => key.toLowerCase().includes(sk.toLowerCase()))) {
      sanitized[key] = '[REDACTED]';
    } else {
      sanitized[key] = value;
    }
  }
  
  return sanitized;
}

async function reportToBackend(error: Error | string, context?: ErrorContext) {
  if (!API_BASE) {
    return;
  }

  try {
    const sanitizedError = typeof error === 'string' 
      ? { message: error }
      : { message: error.message, name: error.name };
    
    await fetch(`${API_BASE}/api/v1/logs/client-error`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: sanitizedError.message,
        name: sanitizedError.name,
        context: sanitizeContext(context),
        timestamp: new Date().toISOString(),
      }),
    });
  } catch (err) {
    // Silently fail - don't log errors about error logging
    if (!isProduction) {
      console.error('Failed to report client error');
    }
  }
}

export async function logClientError(error: Error | string, context?: ErrorContext) {
  const message = typeof error === 'string' ? error : error.message;
  
  // Only log in development
  if (!isProduction) {
    const sanitized = typeof error === 'string' ? error : sanitizeError(error);
    console.error('[Client Error]', message, sanitized);
  }

  // Always report to backend in production
  if (isProduction) {
    await reportToBackend(error, context);
  }
}

export function logWarning(message: string, context?: ErrorContext) {
  if (!isProduction) {
    console.warn('[Client Warning]', message, sanitizeContext(context));
  }
}

export function logInfo(message: string, context?: ErrorContext) {
  if (!isProduction) {
    console.info('[Client Info]', message, sanitizeContext(context));
  }
}

