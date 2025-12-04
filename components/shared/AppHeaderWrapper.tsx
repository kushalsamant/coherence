'use client'

import { usePathname } from 'next/navigation'
import { useSession } from '@/lib/auth-provider'
import Link from 'next/link'
import { AppHeader, buildStandardNavLinks } from '@kushalsamant/design-template'

interface AppHeaderWrapperProps {
  siteName: string
  siteNameHref?: string
  signInHref?: string
}

export default function AppHeaderWrapper({ 
  siteName, 
  siteNameHref = '/',
  signInHref = '/sign-in' 
}: AppHeaderWrapperProps) {
  const pathname = usePathname()
  const { data: session } = useSession()
  const isSignedIn = !!session

  const navLinks = buildStandardNavLinks({
    isSignedIn,
    pricingHref: '/pricing',
    signInHref,
    signOutHref: '/api/auth/signout',
  })

  return (
    <AppHeader
      siteName={siteName}
      siteNameHref={siteNameHref}
      navLinks={navLinks}
      currentPath={pathname}
      LinkComponent={Link}
    />
  )
}

