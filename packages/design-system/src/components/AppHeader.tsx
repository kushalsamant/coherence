'use client'

import React, { useState, useRef, useEffect } from 'react'

export interface NavLink {
  href: string
  label: string
  children?: NavLink[]
}

interface AppHeaderProps {
  siteName?: string
  siteNameHref?: string
  navLinks?: NavLink[]
  leftNavLinks?: NavLink[]
  rightNavLinks?: NavLink[]
  currentPath?: string
  LinkComponent?: React.ComponentType<any>
  onNavClick?: (href: string) => void
}

export default function AppHeader({
  siteName = 'KVSHVL',
  siteNameHref = '/',
  navLinks = [],
  leftNavLinks,
  rightNavLinks,
  currentPath,
  LinkComponent,
  onNavClick,
}: AppHeaderProps) {
  // Use leftNavLinks/rightNavLinks if provided, otherwise fall back to navLinks
  const leftLinks = leftNavLinks || []
  const rightLinks = rightNavLinks || navLinks
  const [openDropdown, setOpenDropdown] = useState<string | null>(null)
  const dropdownRefs = useRef<{ [key: string]: HTMLDivElement | null }>({})

  const Logo = LinkComponent ? (
    <LinkComponent href={siteNameHref} className="logo-link" aria-label="Home">
      <h1 className="logo-text">{siteName}</h1>
    </LinkComponent>
  ) : (
    <a href={siteNameHref} className="logo-link" aria-label="Home">
      <h1 className="logo-text">{siteName}</h1>
    </a>
  )

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      Object.values(dropdownRefs.current).forEach((ref) => {
        if (ref && !ref.contains(event.target as Node)) {
          setOpenDropdown(null)
        }
      })
    }

    if (openDropdown) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [openDropdown])

  const toggleDropdown = (href: string) => {
    setOpenDropdown(openDropdown === href ? null : href)
  }

  const renderNavLink = (link: NavLink) => {
    const isActive = currentPath === link.href || (link.children && link.children.some(child => currentPath === child.href))
    const hasChildren = link.children && link.children.length > 0
    const isDropdownOpen = openDropdown === link.href

    if (hasChildren) {
      return (
        <div
          key={link.href}
          className="nav-dropdown-container"
          ref={(el) => {
            dropdownRefs.current[link.href] = el
          }}
        >
          <button
            className={`nav-dropdown-trigger ${isActive ? 'active' : ''}`}
            onClick={() => toggleDropdown(link.href)}
            aria-expanded={isDropdownOpen}
            aria-haspopup="true"
          >
            {link.label}
            <span className="dropdown-arrow" aria-hidden="true">▼</span>
          </button>
          {isDropdownOpen && (
            <div className="nav-dropdown-menu" role="menu">
              {link.children!.map((child) => {
                const childIsActive = currentPath === child.href
                const childLinkContent = LinkComponent ? (
                  <LinkComponent
                    href={child.href}
                    className="nav-dropdown-item"
                    aria-current={childIsActive ? 'page' : undefined}
                    onClick={() => {
                      onNavClick?.(child.href)
                      setOpenDropdown(null)
                    }}
                    role="menuitem"
                  >
                    {child.label}
                  </LinkComponent>
                ) : (
                  <a
                    href={child.href}
                    className="nav-dropdown-item"
                    aria-current={childIsActive ? 'page' : undefined}
                    onClick={() => {
                      onNavClick?.(child.href)
                      setOpenDropdown(null)
                    }}
                    role="menuitem"
                  >
                    {child.label}
                  </a>
                )
                return (
                  <div key={child.href} className={childIsActive ? 'active' : ''}>
                    {childLinkContent}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )
    }

    // Regular link without dropdown
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
  }

  return (
    <>
      <header className="app-header">
        <div className="header-container">
          <div className="header-content">
            <div className="logo-section">
              {Logo}
            </div>
            {leftLinks.length > 0 && (
              <nav className="desktop-nav desktop-nav-left" aria-label="Left navigation">
                {leftLinks.map((link) => renderNavLink(link))}
              </nav>
            )}
            {rightLinks.length > 0 && (
              <nav className="desktop-nav desktop-nav-right" aria-label="Main navigation">
                {rightLinks.map((link) => renderNavLink(link))}
              </nav>
            )}
          </div>
        </div>
      </header>
    </>
  )
}
