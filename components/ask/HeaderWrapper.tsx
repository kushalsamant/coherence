'use client'

import { usePathname } from 'next/navigation'
import { useSession } from 'next-auth/react'
import Link from 'next/link'
import { AppHeader, buildStandardNavLinks } from '@kushalsamant/design-template'

export default function HeaderWrapper() {
  const pathname = usePathname()
  const { data: session } = useSession()
  const isSignedIn = !!session

  const navLinks = buildStandardNavLinks({
    isSignedIn,
    pricingHref: '/pricing',
    settingsHref: '/settings',
    signInHref: '/sign-in',
    signOutHref: '/api/auth/signout',
  })

  return (
    <AppHeader
      siteName="ASK"
      siteNameHref="/"
      navLinks={navLinks}
      currentPath={pathname}
      LinkComponent={Link}
    />
  )
}

