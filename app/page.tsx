import type { Metadata } from 'next'
import { Card, Button } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Home',
  description: 'Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault. Designing spatial and digital systems—from WikiHouse to research platforms.',
  openGraph: {
    title: 'KVSHVL - Kushal Samant',
    description: 'Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault.',
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
            Licensed Architect. SaaS Developer. Published in MAO Museum. Preserved in Arctic Code Vault.
          </p>
          
          <p className="hero-subtitle" style={{ fontSize: 'var(--font-size-lg)', marginTop: 'var(--space-lg)' }}>
          Designing spatial and digital systems—from WikiHouse to research platforms
          </p>
        </section>

        {/* Products Section */}
        <section className="section" aria-labelledby="products-title">
          <h2 id="products-title" className="section-title">Products</h2>
          
          <div className="grid grid-3">
            <Card
              variant="elevated"
              className="slide-up"
            >
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-sm)' }}>
                  Sketch2BIM
                </h3>
              </div>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)' }}>
                Transform hand-drawn sketches into BIM models. Building information modeling for architectural, landscape, and urban design projects.
              </p>
              <a
                href="https://sketch2bim.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)' }}
              >
                Visit <span aria-hidden="true">→</span>
              </a>
            </Card>

            <Card
              variant="elevated"
              className="slide-up"
            >
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-sm)' }}>
                  ASK
                </h3>
              </div>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)' }}>
                Daily research tool for architecture and sustainability. Offline-first platform for generating photorealistic Q&A content.
              </p>
              <a
                href="https://ask.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)' }}
              >
                Visit <span aria-hidden="true">→</span>
              </a>
            </Card>

            <Card
              variant="elevated"
              className="slide-up"
            >
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-sm)' }}>
                  Reframe
                </h3>
              </div>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)' }}>
                Professional text rewriting with authentic tones. Multiple generation styles for content transformation.
              </p>
              <a
                href="https://reframe.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)' }}
              >
                Visit <span aria-hidden="true">→</span>
              </a>
            </Card>
          </div>
        </section>

        {/* CTA Section */}
        <section className="section">
          <div style={{ textAlign: 'center' }}>
            <Card variant="outlined" className="slide-up">
            <h3 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-md)' }}>
              Need custom SaaS development or technical consulting?
            </h3>
            <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-xl)' }}>
              Let's discuss your project and explore how we can work together.
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
