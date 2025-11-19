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
    <main style={{ padding: '2rem 1rem', maxWidth: '800px', margin: '0 auto' }}>
      <article>
        <h1>Links</h1>
        <p>Connect across platforms</p>
        
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {links.map((link) => (
            <li key={link.name} style={{ marginBottom: '1rem' }}>
              <a 
                href={link.url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ fontSize: '1.125rem' }}
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
