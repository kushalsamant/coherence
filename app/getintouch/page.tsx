import Link from 'next/link'
import type { Metadata } from 'next'
import { Card, Button } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Get in Touch | KVSHVL',
  description: 'Contact for architecture, design, development, and content creation services. Clear engagement process for business inquiries.',
}

export default function GetInTouchPage() {
  const services = [
    {
      title: 'Architecture & Spatial Design',
      description: 'Architectural design, building systems, open-source architecture, competition entries, and spatial planning projects.',
    },
    {
      title: 'SaaS Development & Web Design',
      description: 'Full-stack application development, SaaS platforms, web design, digital marketing automation, and e-commerce solutions.',
    },
    {
      title: 'Design & Creative Work',
      description: 'Graphic design, product design, furniture design, content creation, photography, film making, and sound production.',
    },
    {
      title: 'Teaching & Academic Research',
      description: 'Architectural Design instruction, Graphics & Drawing Representation, AutoDesk products, proofreading research papers, and editing academic work.',
    },
  ]

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <section className="hero" aria-labelledby="contact-title">
          <h1 id="contact-title" className="hero-title">Get in Touch</h1>
          <p className="hero-subtitle">
            Working across architecture, design, development, and content creation since 2006. If you have a project in mind or need expertise in any of these areas, this page outlines how we can work together.
          </p>
        </section>

        <section className="section" aria-labelledby="services-title">
          <h2 id="services-title" className="section-title">Services</h2>
          
          <div className="grid grid-2">
            {services.map((service, index) => (
              <Card
                key={service.title}
                variant="elevated"
                className="slide-up"
              >
                <div>
                    <h3 style={{ 
                      fontSize: 'var(--font-size-xl)', 
                      marginBottom: 'var(--space-sm)',
                    }}>
                      {service.title}
                    </h3>
                    <p style={{ 
                      color: 'var(--color-text-secondary)',
                      margin: 0,
                      lineHeight: 'var(--line-height-relaxed)',
                    }}>
                      {service.description}
                    </p>
                  </div>
              </Card>
            ))}
          </div>
        </section>

        <section className="section" aria-labelledby="contact-methods-title">
          <h2 id="contact-methods-title" className="section-title">How to Contact</h2>
          
          <div className="grid grid-2" style={{ gap: 'var(--space-xl)' }}>
            <Card variant="outlined" className="slide-up">
              <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-md)' }}>
                New Project Inquiries
              </h3>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-md)' }}>
                Email <a href="mailto:writetokushaldsamant@gmail.com">writetokushaldsamant@gmail.com</a> with:
              </p>
              <ul style={{ 
                marginBottom: 'var(--space-md)',
                paddingLeft: 'var(--space-lg)',
                color: 'var(--color-text-secondary)',
              }}>
                <li><strong>Subject:</strong> Project Inquiry - [Your Project Type]</li>
                <li>Brief description of your project</li>
                <li>Timeline and budget expectations</li>
                <li>Your availability for a follow-up discussion</li>
              </ul>
              <p style={{ 
                fontSize: 'var(--font-size-sm)', 
                color: 'var(--color-text-muted)',
                margin: 0,
              }}>
                I respond to serious business inquiries within 48 hours during business days.
              </p>
            </Card>

            <Card variant="outlined" className="slide-up">
              <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-md)' }}>
                Existing Clients
              </h3>
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <p style={{ marginBottom: 'var(--space-sm)' }}>
                  <strong>Phone:</strong><br />
                  <a href="tel:+918779632310">+91 87796 32310</a>
                </p>
                <p style={{ 
                  fontSize: 'var(--font-size-sm)', 
                  color: 'var(--color-text-secondary)',
                  margin: 0,
                }}>
                  <strong>Support Hours:</strong><br />
                  Monday–Saturday, 10:00 AM – 8:00 PM IST
                </p>
              </div>
            </Card>
          </div>

          <div style={{ marginTop: 'var(--space-xl)' }}>
            <Card variant="outlined" className="slide-up">
            <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-md)' }}>
              Quick Questions or Networking
            </h3>
            <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)' }}>
              Connect on <a href="https://linkedin.com/in/kvshvl" target="_blank" rel="noopener noreferrer">LinkedIn</a> for industry discussions and general questions. Please note I don't offer free consultations or exploratory calls.
            </p>
            <Button 
              href="https://linkedin.com/in/kvshvl" 
              variant="secondary"
              target="_blank"
              rel="noopener noreferrer"
            >
              Connect on LinkedIn
            </Button>
          </Card>
          </div>
        </section>
      </article>
    </main>
  )
}
