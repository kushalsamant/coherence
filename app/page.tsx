import type { Metadata } from 'next'
import { Card, Button } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Kushal Samant - Licensed Architect & SaaS Developer',
  description: 'Licensed Architect. SaaS Developer. Published in Future Architecture Platform. Preserved in Arctic Code Vault. Designing spatial and digital systems—from WikiHouse to Sketch2BIM.',
  openGraph: {
    title: 'Kushal Samant - Licensed Architect & SaaS Developer',
    description: 'Licensed Architect. SaaS Developer. Published in Future Architecture Platform. Preserved in Arctic Code Vault. Designing spatial and digital systems—from WikiHouse to Sketch2BIM.',
    type: 'website',
  },
}

export default function Home() {
  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        {/* Hero Section */}
        <section className="hero" aria-labelledby="hero-title">
          <h1 id="hero-title" className="hero-title gradient-text">
            Kushal Samant
          </h1>
          
          <p className="hero-subtitle">
            Licensed Architect. SaaS Developer. Published in Future Architecture Platform. Preserved in Arctic Code Vault.
          </p>
          
          <p className="hero-subtitle" style={{ fontSize: 'var(--font-size-lg)', marginTop: 'var(--space-lg)' }}>
          Designing spatial and digital systems—from WikiHouse to Sketch2BIM
          </p>
        </section>

        {/* CTA Section */}
        <section className="section">
          <div style={{ textAlign: 'center' }}>
            <Card variant="outlined" className="slide-up">
            <h3 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-md)' }}>
              Working across architecture, design, development, and content creation
            </h3>
            <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-xl)' }}>
              Since 2006, I've collaborated on 150+ projects spanning spatial design, open-source building systems, SaaS platforms, and creative content. Let's discuss how we can work together on your project.
            </p>
            <Button href="/getintouch" variant="primary" size="lg">
              Get in Touch
            </Button>
          </Card>
        </div>
        </section>
      </article>
    </main>
  )
}
