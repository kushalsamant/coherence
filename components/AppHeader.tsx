'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import ThemeToggle from './ThemeToggle'

export default function AppHeader() {
  const pathname = usePathname()

  const navLinks = [
    { href: '/getintouch', label: 'Get in Touch' },
    { href: '/history', label: 'History' },
    { href: '/links', label: 'Links' },
  ]

  return (
    <>
      <header className="app-header">
        <div className="header-container">
          <div className="header-content">
            <div className="logo-section">
              <Link href="/" className="logo-link" aria-label="Home">
                <h1 className="logo-text">KVSHVL</h1>
              </Link>
            </div>
            <nav className="desktop-nav" aria-label="Main navigation">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  aria-current={pathname === link.href ? 'page' : undefined}
                >
                  {link.label}
                </Link>
              ))}
              <ThemeToggle />
            </nav>
          </div>
        </div>
      </header>
    </>
  )
}
