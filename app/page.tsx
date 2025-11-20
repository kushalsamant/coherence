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
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article>
        <h1>Kushal Samant</h1>
        
        <p style={{ fontSize: 'var(--font-size-2xl)' }}>
          Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault.<br />
          <br />
          Designing spatial and digital systems—from WikiHouse to AI research platforms
        </p>
        
        <p style={{ fontSize: 'var(--font-size-lg)' }}>
          I work at the intersection of architecture and software development—designing physical spaces and digital systems. Since 2006, I've collaborated internationally on 150+ projects spanning architecture, open-source building systems, and SaaS platforms. My work has been published by MAO Museum and Future Architecture Platform, and one of my repositories is preserved in GitHub's Arctic Code Vault.
        </p>
        
        <hr />
        
        <h2>Explore</h2>
        
        <div>
          <p>
            <strong>History</strong><br />
            Complete archive documenting two decades of work—150+ projects, collaborations, and teaching roles from 2006 to present.
          </p>
          
          <p>
            <strong><a href="https://kvshvl.medium.com" target="_blank" rel="noopener noreferrer">Anthology</a></strong><br />
            Collection of essays exploring architecture, technology, personal philosophy, and the human experience on Medium.
          </p>
          
          <p>
            <strong>Links</strong><br />
            Connect across platforms—GitHub, LinkedIn, Medium, Instagram, and more.
          </p>
        </div>
        
        <hr />
        
        <div>
          <p>
            <strong>Need custom SaaS development or technical consulting?</strong><br />
            Get in Touch to discuss your project.
          </p>
        </div>
      </article>
    </main>
  )
}
