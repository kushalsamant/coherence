import Link from 'next/link'

export default function AppHeader() {
  return (
    <header className="app-header">
      <div className="header-container">
        <div className="header-content">
          <div className="logo-section">
            <Link href="/" className="logo-link">
              <h1 className="logo-text">KVSHVL</h1>
            </Link>
          </div>
          <nav>
            <Link href="/getintouch">Get in Touch</Link>
            <Link href="/history">History</Link>
            <Link href="/links">Links</Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
