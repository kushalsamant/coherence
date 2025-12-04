'use client';

/**
 * Auth Provider for Next Auth v5 (Auth.js)
 * Provides session context to client components
 */

import { SessionProvider } from 'next-auth/react';
import { ReactNode } from 'react';

import { Session } from 'next-auth';

interface AuthProviderProps {
  children: ReactNode;
  session?: Session | null;
}

export function AuthProvider({ children, session }: AuthProviderProps) {
  return <SessionProvider session={session}>{children}</SessionProvider>;
}

// Re-export commonly used hooks and functions for convenience
export { useSession, signIn, signOut } from 'next-auth/react';

