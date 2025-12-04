'use client'

import { usePathname } from 'next/navigation'
import { useSession } from '@/lib/auth-provider'
import Link from 'next/link'
import { AppHeader, buildStandardNavLinks } from '@kushalsamant/design-template'

export default function HeaderWrapper() {
  const pathname = usePathname()
  const { data: session } = useSession()
  const isSignedIn = !!session

  const navLinks = buildStandardNavLinks({
    isSignedIn,
    pricingHref: '/pricing',
    signInHref: '/api/auth/signin',
    signOutHref: '/api/auth/signout',
  })

  return (
    <AppHeader
      siteName="Sketch-to-BIM"
      siteNameHref="/"
      navLinks={navLinks}
      currentPath={pathname}
      LinkComponent={Link}
    />
  )
}

