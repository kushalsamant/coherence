import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
  description: 'Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault. Designing spatial and digital systems—from WikiHouse to AI research platforms.',
  openGraph: {
    title: 'KVSHVL - Kushal Samant',
    description: 'Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault.',
    type: 'website',
  },
}

export default function Home() {
  return (
    <main style={{ padding: '2rem 1rem' }}>
      <article>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '1rem' }}>
          Kushal Samant
        </h1>
        
        <p style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>
          Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault.<br />
          <br />
          Designing spatial and digital systems—from WikiHouse to AI research platforms
        </p>
        
        <p style={{ fontSize: '1.125rem', marginBottom: '2rem' }}>
          I work at the intersection of architecture and software development—designing physical spaces and digital systems. Since 2006, I've collaborated internationally on 150+ projects spanning architecture, open-source building systems, and SaaS platforms. My work has been published by MAO Museum and Future Architecture Platform, and one of my repositories is preserved in GitHub's Arctic Code Vault.
        </p>
        
        <hr style={{ margin: '2rem 0', border: 'none', borderTop: '1px solid #444444' }} />
        
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem' }}>Explore</h2>
        
        <div style={{ marginBottom: '2rem' }}>
          <p style={{ marginBottom: '1rem' }}>
            <strong><Link href="/history">History</Link></strong><br />
            Complete archive documenting two decades of work—150+ projects, collaborations, and teaching roles from 2006 to present.
          </p>
          
          <p style={{ marginBottom: '1rem' }}>
            <strong><a href="https://kvshvl.medium.com" target="_blank" rel="noopener noreferrer">Anthology</a></strong><br />
            Collection of essays exploring architecture, technology, personal philosophy, and the human experience on Medium.
          </p>
          
          <p style={{ marginBottom: '1rem' }}>
            <strong><Link href="/links">Links</Link></strong><br />
            Connect across platforms—GitHub, LinkedIn, Medium, Instagram, and more.
          </p>
        </div>
        
        <hr style={{ margin: '2rem 0', border: 'none', borderTop: '1px solid #444444' }} />
        
        <div>
          <p>
            <strong>Need custom SaaS development or technical consulting?</strong><br />
            <Link href="/getintouch">Get in Touch</Link> to discuss your project.
          </p>
        </div>
      </article>
    </main>
  )
}
