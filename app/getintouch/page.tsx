import Link from 'next/link'
import type { Metadata } from 'next'
import { Card, Button } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Get in Touch | KVSHVL',
  description: 'Contact for SaaS development and technical consulting. Clear engagement process for business inquiries.',
}

export default function GetInTouchPage() {
  const services = [
    {
      title: 'Custom SaaS Development',
      description: 'Full-stack application development, cloud solutions, API integration, database architecture, DevOps.',
    },
    {
      title: 'SaaS Subscriptions',
      description: 'Monthly/annual access to proprietary software platforms for individuals, businesses, and enterprises.',
    },
    {
      title: 'Technical Consulting',
      description: 'Architecture planning, technology selection, scalability assessments, security consulting, technical due diligence.',
    },
    {
      title: 'Compliance & Security',
      description: 'GDPR (EU), CCPA (California), Indian IT Act 2000 compliant. SOC 2 Type II, ISO 27001 practices. HIPAA solutions available with BAA.',
    },
  ]

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <section className="hero" aria-labelledby="contact-title">
          <h1 id="contact-title" className="hero-title">Get in Touch</h1>
          <p className="hero-subtitle">
            I work with businesses on custom SaaS development, technical consulting, and cloud solutions. If you have a project in mind or need technical expertise, this page outlines how we can work together.
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
