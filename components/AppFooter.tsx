import Link from 'next/link'

export default function AppFooter() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="app-footer" role="contentinfo">
      <div className="footer-container">
        <div className="footer-links">
          <span className="footer-link">
            <Link href="/links">Links</Link>
          </span>
          <span className="link-separator">|</span>
          <span className="footer-link">
            <Link href="/privacypolicy">Privacy Policy</Link>
          </span>
          <span className="link-separator">|</span>
          <span className="footer-link">
            <Link href="/termsofservice">Terms of Service</Link>
          </span>
        </div>
        <div className="footer-branding">
          © {currentYear} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.
        </div>
      </div>
    </footer>
  )
}
