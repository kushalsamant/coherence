import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Get in Touch | KVSHVL',
  description: 'Contact for SaaS development and technical consulting. Clear engagement process for business inquiries.',
}

export default function GetInTouchPage() {
  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article>
        <h1>Get in Touch</h1>
        
        <p>
          I work with businesses on custom SaaS development, technical consulting, and cloud solutions. If you have a project in mind or need technical expertise, this page outlines how we can work together.
        </p>
        
        <hr />
        
        <section>
          <h2>Services</h2>
          
          <p>
            <strong>Custom SaaS Development</strong> - Full-stack application development, cloud solutions, API integration, database architecture, DevOps.
          </p>
          
          <p>
            <strong>SaaS Subscriptions</strong> - Monthly/annual access to proprietary software platforms for individuals, businesses, and enterprises.
          </p>
          
          <p>
            <strong>Technical Consulting</strong> - Architecture planning, technology selection, scalability assessments, security consulting, technical due diligence.
          </p>
          
          <p>
            <strong>Compliance & Security</strong> - GDPR (EU), CCPA (California), Indian IT Act 2000 compliant. SOC 2 Type II, ISO 27001 practices. HIPAA solutions available with BAA.
          </p>
        </section>
        
        <hr />
        
        <section>
          <h2>How to Contact</h2>
          
          <h3>For New Project Inquiries</h3>
          <p>
            Email <a href="mailto:writetokushaldsamant@gmail.com">writetokushaldsamant@gmail.com</a> with:
          </p>
          <ul>
            <li><strong>Subject:</strong> Project Inquiry - [Your Project Type]</li>
            <li>Brief description of your project</li>
            <li>Timeline and budget expectations</li>
            <li>Your availability for a follow-up discussion</li>
          </ul>
          <p>I respond to serious business inquiries within 48 hours during business days.</p>
          
          <h3>For Existing Clients</h3>
          <p>
            <strong>Phone:</strong> +91 87796 32310<br />
            <strong>Support Hours:</strong> Monday–Saturday, 10:00 AM – 8:00 PM IST
          </p>
          
          <h3>For Quick Questions or Networking</h3>
          <p>
            Connect on <a href="https://linkedin.com/in/kvshvl" target="_blank" rel="noopener noreferrer">LinkedIn</a> for industry discussions and general questions. Please note I don't offer free consultations or exploratory calls.
          </p>
        </section>
      </article>
    </main>
  )
}
