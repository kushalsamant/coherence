import React, { type ReactNode } from 'react'

interface TestimonialProps {
  quote: string | ReactNode
  author: string
  role?: string
  company?: string
  className?: string
}

export default function Testimonial({
  quote,
  author,
  role,
  company,
  className = '',
}: TestimonialProps) {
  return (
    <figure className={className}>
      <blockquote style={{
        borderLeft: '2px solid var(--color-text)',
        margin: 'var(--space-xl) 0',
        padding: '0 var(--space-xl)',
        fontStyle: 'italic',
        fontSize: 'var(--font-size-lg)',
        lineHeight: 'var(--line-height-relaxed)',
        color: 'var(--color-text-secondary)',
      }}>
        {typeof quote === 'string' ? <p>{quote}</p> : quote}
      </blockquote>
      <figcaption style={{
        marginTop: 'var(--space-lg)',
        paddingLeft: 'var(--space-xl)',
      }}>
        <div style={{ fontWeight: 'var(--font-weight-semibold)' }}>
          {author}
        </div>
        {(role || company) && (
          <div style={{ 
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
          }}>
            {role && <span>{role}</span>}
            {role && company && <span>, </span>}
            {company && <span>{company}</span>}
          </div>
        )}
      </figcaption>
    </figure>
  )
}

