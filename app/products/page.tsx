import type { Metadata } from 'next'
import { Card, Button } from '@kushalsamant/design-template'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Products - Sketch2BIM',
  description: 'Transform hand-drawn architectural sketches into BIM models. Building information modeling for architectural, landscape, urban design, and urban planning projects.',
  openGraph: {
    title: 'Products - Sketch2BIM',
    description: 'Transform hand-drawn architectural sketches into BIM models. Building information modeling for architectural, landscape, urban design, and urban planning projects.',
    type: 'website',
  },
}

export default function Products() {
  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <section className="section" aria-labelledby="product-title">
          <h2 id="product-title" className="section-title">Sketch2BIM</h2>
          
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <Card
              variant="elevated"
              className="slide-up"
              href="https://sketch2bim.kvshvl.in"
              LinkComponent={Link}
            >
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <h3 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-sm)' }}>
                  Transform Hand-Drawn Sketches into BIM Models
                </h3>
              </div>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)', fontSize: 'var(--font-size-lg)' }}>
                Building information modeling for architectural, landscape, urban design, and urban planning projects. Convert your sketches into industry-standard IFC, DWG, RVT, and SKP formats.
              </p>
              <div style={{ marginTop: 'var(--space-xl)' }}>
                <Button variant="primary" size="lg">
                  Get Started
                </Button>
              </div>
            </Card>
          </div>
        </section>
      </article>
    </main>
  )
}
