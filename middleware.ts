import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Middleware for unified platform subscription checking
// Checks subscription status for app routes
//
// NOTE: Next.js 16 shows deprecation warning for middleware.ts
// However, this is still the official pattern as of Next.js 16.0.7
// The "proxy" pattern mentioned in the warning is not yet documented
// Monitor: https://nextjs.org/docs/messages/middleware-to-proxy
// TODO: Migrate when official migration path is available

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip middleware for public routes
  if (
    pathname.startsWith('/api/auth') ||
    pathname.startsWith('/api/subscriptions/checkout') ||
    pathname.startsWith('/api/subscriptions/webhook') ||
    pathname === '/' ||
    pathname.startsWith('/subscribe') ||
    pathname.startsWith('/account') ||
    pathname.startsWith('/getintouch') ||
    pathname.startsWith('/history') ||
    pathname.startsWith('/projects') ||
    pathname.startsWith('/links') ||
    pathname.startsWith('/privacypolicy') ||
    pathname.startsWith('/termsofservice') ||
    pathname.startsWith('/cancellationrefund')
  ) {
    return NextResponse.next();
  }

  // For app routes (/ask, /reframe, /sketch2bim)
  // Subscription checking is handled at the API level for each request
  // This allows for more flexible access control and better error handling
  if (
    pathname.startsWith('/ask') ||
    pathname.startsWith('/reframe') ||
    pathname.startsWith('/sketch2bim')
  ) {
    // Allow access - individual API routes handle subscription validation
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};

