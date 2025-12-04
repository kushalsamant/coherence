'use client'

import React from 'react'
import ThemeToggle from './ThemeToggle'

export interface NavLink {
  href: string
  label: string
}

interface AppHeaderProps {
  siteName?: string
  siteNameHref?: string
  navLinks?: NavLink[]
  currentPath?: string
  LinkComponent?: React.ComponentType<any>
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
          </div>
        </div>
      </header>
    </>
  )
}
