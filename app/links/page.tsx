import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Links | KVSHVL',
  description: 'Connect across platforms—GitHub, LinkedIn, Medium, Instagram, and more.',
}

export default function LinksPage() {
  const links = [
    { name: 'GitHub', url: 'https://github.com/kushalsamant' },
    { name: 'LinkedIn', url: 'https://linkedin.com/in/kvshvl' },
    { name: 'Medium', url: 'https://kvshvl.medium.com' },
    { name: 'Instagram', url: 'https://instagram.com/kvshvl' },
    { name: 'Twitter', url: 'https://twitter.com/kvshvl_' },
    { name: 'YouTube', url: 'https://youtube.com/@kvshvl' },
  ]

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article>
        <h1>Links</h1>
        <p>Connect across platforms</p>
        
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {links.map((link) => (
            <li key={link.name} style={{ marginBottom: 'var(--space-lg)' }}>
              <a 
                href={link.url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ fontSize: 'var(--font-size-xl)' }}
              >
                {link.name}
              </a>
            </li>
          ))}
        </ul>
      </article>
    </main>
  )
}
