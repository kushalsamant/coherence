'use client'

import { useSession } from '@/lib/auth-provider'
import Link from 'next/link'
import { signIn, signOut } from '@/auth'

export default function HeaderWrapper() {
  const { data: session } = useSession()

  return (
    <header className="border-b border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">
          {{APP_DISPLAY_NAME}}
        </Link>
        <nav className="flex items-center gap-4">
          <Link href="/pricing" className="hover:text-primary transition-colors">
            Pricing
          </Link>
          {session ? (
            <>
              <Link href="/settings" className="hover:text-primary transition-colors">
                Settings
              </Link>
              <button
                onClick={() => signOut()}
                className="px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              >
                Sign Out
              </button>
            </>
          ) : (
            <button
              onClick={() => signIn()}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              Sign In
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}

