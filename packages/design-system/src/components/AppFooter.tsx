import React from 'react'
import type { NavLink } from './AppHeader'

interface FooterLink {
  href: string
  label: string
}

interface AppFooterProps {
  legalLinks?: FooterLink[]
  socialLinks?: Array<{ href: string; label: string }>
  branding?: React.ReactNode
  companyLink?: string
  companyLabel?: string
  className?: string
  LinkComponent?: React.ComponentType<any>
}

export default function AppFooter({
  legalLinks = [],
  socialLinks,
  branding,
  companyLink,
  companyLabel = 'KVSHVL',
  className = '',
  LinkComponent,
}: AppFooterProps) {
  const currentYear = new Date().getFullYear()

  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <footer className={`app-footer ${className}`.trim()} role="contentinfo">
      <div className="footer-container">
        <div className="footer-content">
          {legalLinks.length > 0 && (
            <div className="footer-links">
              {legalLinks.map((link, index) => (
                <span key={link.href}>
                  <Link href={link.href} className="footer-link">
                    {link.label}
                  </Link>
                  {index < legalLinks.length - 1 && (
                    <span className="link-separator" aria-hidden="true">|</span>
                  )}
                </span>
              ))}
            </div>
          )}
          
          {socialLinks && socialLinks.length > 0 && (
            <div className="footer-links" style={{ marginTop: 'var(--space-md)' }}>
              {socialLinks.map((link, index) => (
                <span key={link.href}>
                  <Link
                    href={link.href}
                    className="footer-link"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {link.label}
                  </Link>
                  {index < socialLinks.length - 1 && (
                    <span className="link-separator" aria-hidden="true">|</span>
                  )}
                </span>
              ))}
            </div>
          )}
          
          {branding && (
            <div className="footer-branding">
              {typeof branding === 'string' 
                ? branding.replace('{year}', currentYear.toString())
                : branding}
            </div>
          )}
          
          {companyLink && (
            <div className="footer-company" style={{ marginTop: 'var(--space-md)' }}>
              Made with &lt;3 by{' '}
              <Link
                href={companyLink}
                className="footer-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                {companyLabel}
              </Link>
            </div>
          )}
        </div>
      </div>
    </footer>
  )
}
