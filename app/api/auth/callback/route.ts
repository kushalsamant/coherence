import { createRouteHandlerClient } from '@/lib/auth';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  const returnUrl = requestUrl.searchParams.get('returnUrl');

  if (code) {
    const supabase = createRouteHandlerClient(request);
    await supabase.auth.exchangeCodeForSession(code);
  }

  // Redirect to returnUrl if provided, otherwise to home page
  if (returnUrl) {
    try {
      const decodedReturnUrl = decodeURIComponent(returnUrl);
      return NextResponse.redirect(decodedReturnUrl);
    } catch (error) {
      // If returnUrl is invalid, fall back to home page
      return NextResponse.redirect(new URL('/', requestUrl.origin));
    }
  }

  // Default: redirect to home page after successful authentication
  return NextResponse.redirect(new URL('/', requestUrl.origin));
}

