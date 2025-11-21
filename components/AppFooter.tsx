import Link from 'next/link'

export default function AppFooter() {
  const currentYear = new Date().getFullYear()

  const legalLinks = [
    { href: '/privacypolicy', label: 'Privacy Policy' },
    { href: '/termsofservice', label: 'Terms of Service' },
    { href: '/cancellationrefund', label: 'Cancellation & Refund' },
  ]

  return (
    <footer className="app-footer" role="contentinfo">
      <div className="footer-container">
        <div className="footer-content">
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
          <div className="footer-branding">
            © {currentYear} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.
          </div>
        </div>
      </div>
    </footer>
  )
}
