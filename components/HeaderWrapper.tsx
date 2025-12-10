'use client'

import { usePathname } from 'next/navigation'
import { useAuth } from '@/lib/auth-provider'
import Link from 'next/link'
import { AppHeader } from '@kushalsamant/design-template'

export default function HeaderWrapper() {
  const pathname = usePathname()
  const { user, signOut } = useAuth()
  const isSignedIn = !!user
  const isProductsPage = pathname === '/products'

  // Build navigation links
  const navLinks = []
  
  if (isProductsPage) {
    // On products page: show Products, Pricing, and Account on the right
    navLinks.push(
      { href: '/products', label: 'Products' },
      { href: '/subscribe', label: 'Pricing' },
      { href: '/account', label: 'Account' }
    )
  } else {
    // On other pages: show Products link only
    navLinks.push({ href: '/products', label: 'Products' })
  }
  
  // Add Sign Out when signed in (as a button handler, not a link)
  // Note: We'll handle sign out via onClick in the AppHeader component if needed
  
  return (
    <AppHeader
      siteName="KVSHVL"
      siteNameHref="/"
      navLinks={navLinks}
      currentPath={pathname}
      LinkComponent={Link}
    />
  )
}

