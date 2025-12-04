'use client';

type ErrorContext = Record<string, unknown> | undefined;

const isProduction = process.env.NODE_ENV === 'production';

const API_BASE = process.env.SKETCH2BIM_NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_URL;

// Strip sensitive data from error objects
function sanitizeError(error: unknown): Record<string, unknown> {
  if (!error || typeof error !== 'object') return {};
  
  // Create a sanitized copy
  const sanitized: Record<string, unknown> = {};
  const err = error as Record<string, unknown>;
  
  // Only include safe fields
  if ('message' in err && typeof err.message === 'string') sanitized.message = err.message;
  if ('name' in err && typeof err.name === 'string') sanitized.name = err.name;
  if ('code' in err) sanitized.code = err.code;
  if ('status' in err) sanitized.status = err.status;
  
  // Sanitize response context
  if ('response' in err && err.response && typeof err.response === 'object') {
    const response = err.response as Record<string, unknown>;
    sanitized.response = {
      status: response.status,
      statusText: response.statusText,
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
    // Silently fail - don't log errors about error logging in production
  }
}

export async function logClientError(error: Error | string, context?: ErrorContext) {
  // Report to backend in production
  if (isProduction) {
    await reportToBackend(error, context);
  }
  // Development logging handled by backend
}

export function logWarning(message: string, context?: ErrorContext) {
  // Warnings are handled by backend logging
}

export function logInfo(message: string, context?: ErrorContext) {
  // Info logs are handled by backend logging
}

