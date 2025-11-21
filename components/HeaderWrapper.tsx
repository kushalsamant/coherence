'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { AppHeader } from '@kushalsamant/design-template'

const navLinks = [
  { href: '/history', label: 'History' },
]

export default function HeaderWrapper() {
  const pathname = usePathname()
  
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

