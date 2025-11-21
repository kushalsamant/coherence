'use client'

import React, { useState } from 'react'
import type { ReactNode } from 'react'
import ThemeToggle from './ThemeToggle'
import MobileMenu from './MobileMenu'

export interface NavLink {
  href: string
  label: string
}

interface AppHeaderProps {
  siteName?: string
  siteNameHref?: string
  navLinks?: NavLink[]
  currentPath?: string
  LinkComponent?: React.ComponentType<{ href: string; className?: string; 'aria-label'?: string; children: ReactNode }>
  onNavClick?: (href: string) => void
}

export default function AppHeader({
  siteName = 'KVSHVL',
  siteNameHref = '/',
  navLinks = [],
  currentPath,
  LinkComponent,
  onNavClick,
}: AppHeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const Logo = LinkComponent ? (
    <LinkComponent href={siteNameHref} className="logo-link" aria-label="Home">
      <h1 className="logo-text">{siteName}</h1>
    </LinkComponent>
  ) : (
    <a href={siteNameHref} className="logo-link" aria-label="Home">
      <h1 className="logo-text">{siteName}</h1>
    </a>
  )

  return (
    <>
      <header className="app-header">
        <div className="header-container">
          <div className="header-content">
            <div className="logo-section">
              {Logo}
            </div>
            <nav className="desktop-nav" aria-label="Main navigation">
              {navLinks.map((link) => {
                const isActive = currentPath === link.href
                const linkContent = LinkComponent ? (
                  <LinkComponent
                    href={link.href}
                    aria-current={isActive ? 'page' : undefined}
                    onClick={() => onNavClick?.(link.href)}
                  >
                    {link.label}
                  </LinkComponent>
                ) : (
                  <a
                    href={link.href}
                    aria-current={isActive ? 'page' : undefined}
                    onClick={() => onNavClick?.(link.href)}
                  >
                    {link.label}
                  </a>
                )
                return <span key={link.href}>{linkContent}</span>
              })}
              <ThemeToggle />
            </nav>
            <button
              className="mobile-menu-toggle"
              onClick={() => setMobileMenuOpen(true)}
              aria-label="Open menu"
              aria-expanded={mobileMenuOpen}
            >
              <span aria-hidden="true">☰</span>
            </button>
          </div>
        </div>
      </header>
      <MobileMenu
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        navLinks={navLinks}
        currentPath={currentPath}
        LinkComponent={LinkComponent}
        onNavClick={onNavClick}
      />
    </>
  )
}

