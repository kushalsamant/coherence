'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect } from 'react'

interface MobileMenuProps {
  isOpen: boolean
  onClose: () => void
}

export default function MobileMenu({ isOpen, onClose }: MobileMenuProps) {
  const pathname = usePathname()

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen])

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  const navLinks = [
    { href: '/getintouch', label: 'Get in Touch' },
    { href: '/history', label: 'History' },
    { href: '/links', label: 'Links' },
  ]

  return (
    <div className={`mobile-menu ${isOpen ? 'active' : ''}`} onClick={onClose}>
      <div className="mobile-menu-content" onClick={(e) => e.stopPropagation()}>
        <button
          className="mobile-menu-close"
          onClick={onClose}
          aria-label="Close menu"
          type="button"
        >
          ×
        </button>
        <nav aria-label="Main navigation">
          <Link 
            href="/" 
            aria-current={pathname === '/' ? 'page' : undefined}
            onClick={onClose}
          >
            Home
          </Link>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href ? 'page' : undefined}
              onClick={onClose}
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </div>
  )
}

