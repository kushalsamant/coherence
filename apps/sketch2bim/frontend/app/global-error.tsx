'use client';

import { useEffect } from 'react';
import { logClientError } from '@/lib/errorLogger';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error via the open-source logger
    logClientError(error, { source: 'global-error' });
  }, [error]);

  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
          <div className="max-w-md w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8 text-center">
            <div className="mb-4">
              <svg
                className="mx-auto h-12 w-12 text-red-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
              Something went wrong!
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              We encountered an unexpected error. Our team has been notified.
            </p>
            {error.digest && (
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">
                Error ID: {error.digest}
              </p>
            )}
            <div className="flex gap-4 justify-center">
              <button
                onClick={reset}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Try again
              </button>
              <a
                href="/"
                className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Go home
              </a>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}

