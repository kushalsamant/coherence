/**
 * Error handling utilities for Reframe
 */

export interface ErrorWithMessage {
  message: string
}

export function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as Record<string, unknown>).message === 'string'
  )
}

export function toErrorWithMessage(maybeError: unknown): ErrorWithMessage {
  if (isErrorWithMessage(maybeError)) return maybeError

  try {
    return { message: JSON.stringify(maybeError) }
  } catch {
    // fallback in case there's an error stringifying
    return { message: String(maybeError) }
  }
}

export function getErrorMessage(error: unknown): string {
  return toErrorWithMessage(error).message
}

