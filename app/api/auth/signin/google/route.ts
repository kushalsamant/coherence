import { NextRequest, NextResponse } from 'next/server';

/**
 * Google OAuth sign-in route handler
 * Redirects to the sign-in page with query parameters preserved
 * This route is called by shared-frontend auth package
 */
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const app = searchParams.get('app');
  const returnUrl = searchParams.get('returnUrl');

  // Redirect to the sign-in page with query parameters
  const signInUrl = new URL('/api/auth/signin', request.nextUrl.origin);
  if (app) {
    signInUrl.searchParams.set('app', app);
  }
  if (returnUrl) {
    signInUrl.searchParams.set('returnUrl', returnUrl);
  }

  return NextResponse.redirect(signInUrl);
}

export async function POST(request: NextRequest) {
  // Handle POST requests the same way as GET
  return GET(request);
}

