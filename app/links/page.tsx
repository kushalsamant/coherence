import type { Metadata } from 'next'
import { Card } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Links | KVSHVL',
  description: 'Connect across platforms—GitHub, LinkedIn, Medium, Instagram, and more.',
}

export default function LinksPage() {
  const links = [
    { 
      name: 'GitHub', 
      url: 'https://github.com/kushalsamant',
      description: 'Open-source projects and code repositories',
    },
    { 
      name: 'LinkedIn', 
      url: 'https://linkedin.com/in/kvshvl',
      description: 'Professional network and career updates',
    },
    { 
      name: 'Medium', 
      url: 'https://kvshvl.medium.com',
      description: 'Essays on architecture, technology, and philosophy',
    },
    { 
      name: 'Instagram', 
      url: 'https://instagram.com/kvshvl',
      description: 'Visual portfolio and design inspiration',
    },
    { 
      name: 'Twitter', 
      url: 'https://twitter.com/kvshvl_',
      description: 'Thoughts, updates, and industry insights',
    },
    { 
      name: 'YouTube', 
      url: 'https://youtube.com/@kvshvl',
      description: 'Video content and tutorials',
    },
  ]

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <section className="hero" aria-labelledby="links-title">
          <h1 id="links-title" className="hero-title">Links</h1>
          <p className="hero-subtitle">Connect across platforms</p>
        </section>

        <section className="section" aria-labelledby="products-section-title">
          <h2 id="products-section-title" className="section-title">Products</h2>
          
          <div className="grid grid-2" style={{ marginBottom: 'var(--space-3xl)' }}>
            <Card
              variant="elevated"
              className="slide-up"
            >
              <a
                href="https://sketch2bim.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ 
                  display: 'flex',
                  flexDirection: 'column',
                  textDecoration: 'none',
                  color: 'inherit',
                  height: '100%',
                }}
              >
                <h3 style={{ 
                  fontSize: 'var(--font-size-xl)', 
                  marginBottom: 'var(--space-xs)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-xs)',
                }}>
                  Sketch2BIM
                  <span aria-hidden="true" style={{ fontSize: 'var(--font-size-sm)', opacity: 0.6 }}>
                    →
                  </span>
                </h3>
                <p style={{ 
                  color: 'var(--color-text-secondary)',
                  fontSize: 'var(--font-size-sm)',
                  margin: 0,
                }}>
                  Transform sketches into BIM models
                </p>
              </a>
            </Card>

            <Card
              variant="elevated"
              className="slide-up"
            >
              <a
                href="https://ask.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ 
                  display: 'flex',
                  flexDirection: 'column',
                  textDecoration: 'none',
                  color: 'inherit',
                  height: '100%',
                }}
              >
                <h3 style={{ 
                  fontSize: 'var(--font-size-xl)', 
                  marginBottom: 'var(--space-xs)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-xs)',
                }}>
                  Ask AI
                  <span aria-hidden="true" style={{ fontSize: 'var(--font-size-sm)', opacity: 0.6 }}>
                    →
                  </span>
                </h3>
                <p style={{ 
                  color: 'var(--color-text-secondary)',
                  fontSize: 'var(--font-size-sm)',
                  margin: 0,
                }}>
                  Daily research tool for architecture
                </p>
              </a>
            </Card>

            <Card
              variant="elevated"
              className="slide-up"
            >
              <a
                href="https://reframe.kvshvl.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ 
                  display: 'flex',
                  flexDirection: 'column',
                  textDecoration: 'none',
                  color: 'inherit',
                  height: '100%',
                }}
              >
                <h3 style={{ 
                  fontSize: 'var(--font-size-xl)', 
                  marginBottom: 'var(--space-xs)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-xs)',
                }}>
                  Reframe AI
                  <span aria-hidden="true" style={{ fontSize: 'var(--font-size-sm)', opacity: 0.6 }}>
                    →
                  </span>
                </h3>
                <p style={{ 
                  color: 'var(--color-text-secondary)',
                  fontSize: 'var(--font-size-sm)',
                  margin: 0,
                }}>
                  Professional text rewriting platform
                </p>
              </a>
            </Card>
          </div>
        </section>

        <section className="section" aria-labelledby="social-links-title">
          <h2 id="social-links-title" className="section-title">Social Links</h2>
          <div className="grid grid-2">
            {links.map((link, index) => (
              <Card
                key={link.url}
                variant="elevated"
                className="slide-up"
              >
                <a
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ 
                    display: 'flex',
                    flexDirection: 'column',
                    textDecoration: 'none',
                    color: 'inherit',
                    height: '100%',
                  }}
                >
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 'var(--space-md)',
                    marginBottom: 'var(--space-md)',
                  }}>
                    <div>
                      <h3 style={{ 
                        fontSize: 'var(--font-size-xl)', 
                        marginBottom: 'var(--space-xs)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 'var(--space-xs)',
                      }}>
                        {link.name}
                        <span aria-hidden="true" style={{ fontSize: 'var(--font-size-sm)', opacity: 0.6 }}>
                          →
                        </span>
                      </h3>
                      <p style={{ 
                        color: 'var(--color-text-secondary)',
                        fontSize: 'var(--font-size-sm)',
                        margin: 0,
                      }}>
                        {link.description}
                      </p>
                    </div>
                  </div>
                </a>
              </Card>
            ))}
          </div>
        </section>
      </article>
    </main>
  )
}
