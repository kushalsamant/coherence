import { auth } from "@/auth";
import { NextResponse } from "next/server";

// Define public routes that don't require authentication
const publicRoutes = [
  '/',
  '/sign-in',
  '/sign-up',
  '/pricing',
  '/terms',
  '/privacy',
  '/api/razorpay-webhook', // Razorpay webhooks should be public
  '/api/auth', // Auth.js API routes
];

export default auth((req) => {
  const { pathname } = req.nextUrl;
  
  // Check if the route is public
  const isPublicRoute = publicRoutes.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );
  
  // Redirect authenticated users away from sign-in/sign-up pages
  if (req.auth && (pathname === '/sign-in' || pathname === '/sign-up')) {
    return NextResponse.redirect(new URL('/', req.url));
  }
  
  // If it's a public route or user is authenticated, allow access
  if (isPublicRoute || req.auth) {
    return NextResponse.next();
  }
  
  // Redirect to sign-in if not authenticated
  const signInUrl = new URL('/sign-in', req.url);
  signInUrl.searchParams.set('callbackUrl', pathname);
  return NextResponse.redirect(signInUrl);
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};

