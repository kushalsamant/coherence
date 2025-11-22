import type { Metadata } from 'next'
import Link from 'next/link'
import Image from 'next/image'
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
          
          <div style={{ marginTop: 'var(--space-xl)' }}>
            <Button href="/history" variant="secondary" size="lg">
              View Complete History
            </Button>
          </div>
        </section>
        
        {/* About Section */}
        <section className="section slide-up" aria-labelledby="about-title" style={{ animationDelay: '0.1s' }}>
          <h2 id="about-title" className="section-title">About</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', alignItems: 'flex-start' }}>
            <Image
              src="/assets/img/logo_kushal_samant_profile_picture_white.png"
              alt="Architect Kushal Dhananjay Samant"
              width={150}
              height={150}
              style={{ borderRadius: 'var(--radius-lg)', marginBottom: 'var(--space-md)', maxWidth: '100%', height: 'auto' }}
            />
            
            <div style={{ maxWidth: '65ch', width: '100%' }}>
              <p style={{ fontSize: 'var(--font-size-lg)', lineHeight: 'var(--line-height-relaxed)', marginBottom: 'var(--space-lg)' }}>
                Kushal Dhananjay Samant is an Architect, based in India.
              </p>
              
              <p style={{ fontSize: 'var(--font-size-base)', lineHeight: 'var(--line-height-relaxed)', marginBottom: 'var(--space-md)' }}>
                In 2006, I started this journey as a side-hustle by selling stationery. Since then, I've collaborated internationally on 150+ projects spanning architecture, open-source building systems, and SaaS platforms.
              </p>
              
              <p style={{ fontSize: 'var(--font-size-base)', lineHeight: 'var(--line-height-relaxed)', marginBottom: 'var(--space-md)' }}>
                In 2015, I started the WikiHouse / BOM chapter of <a href="https://www.wikihouse.cc" rel="noopener noreferrer" target="_blank">The WikiHouse Project</a> in Bombay. In 2016, <a href="http://www.mao.si" rel="noopener noreferrer" target="_blank">Muzej Za Arhitektiro In Oblikovanje</a> and <a href="https://www.futurearchitectureplatform.org/projects/8e8af477-4aea-431b-a69f-74cd05862eac" rel="noopener noreferrer" target="_blank">Future Architecture Platform</a> published my work: <a href="https://kushalsamant.github.io/projects/gruham.html" rel="noopener noreferrer" target="_blank">GRÜHAM</a>.
              </p>
              
              <p style={{ fontSize: 'var(--font-size-base)', lineHeight: 'var(--line-height-relaxed)', marginBottom: 'var(--space-md)' }}>
                In 2020, one of my repositories was selected for the <a href="https://youtu.be/fzI9FNjXQ0o" rel="noopener noreferrer" target="_blank">Arctic Code Vault</a> of the <a href="https://archiveprogram.github.com" rel="noopener noreferrer" target="_blank">GitHub Archive Program</a>. Since 2022, I am listed as an Assistant Professor of Architecture at Dr. D.Y. Patil School of Architecture, Navi Mumbai.
              </p>
              
              <p style={{ fontSize: 'var(--font-size-base)', lineHeight: 'var(--line-height-relaxed)', marginBottom: 'var(--space-lg)' }}>
                Currently, I am creating the open-source <a href="https://github.com/kushalsamant/ask" rel="noopener noreferrer" target="_blank">ASK: Daily Research</a> tool—an offline-first AI platform for generating photorealistic Q&A content on research themes including architecture, sustainability, and urban planning.
              </p>
              
              <Link href="/history" style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)', fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-medium)' }}>
                Read the complete history <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
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
