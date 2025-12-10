// Legacy NextAuth route - replaced with Supabase Auth
// This file is kept for backward compatibility during migration
// All auth routes are now handled by Supabase Auth

import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.redirect('/api/auth/signin');
}

export async function POST() {
  return NextResponse.json({ error: 'NextAuth is deprecated. Use Supabase Auth instead.' }, { status: 410 });
}
