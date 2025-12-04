import React, { type ReactNode } from 'react'
import Button from './Button'

interface HeroProps {
  title: string
  tagline?: string
  description?: string
  cta?: {
    label: string
    href?: string
    onClick?: () => void
    variant?: 'primary' | 'secondary' | 'ghost'
  }
  className?: string
  LinkComponent?: React.ComponentType<any>
}

export default function Hero({
  title,
  tagline,
  description,
  cta,
  className = '',
  LinkComponent,
}: HeroProps) {
  return (
    <section className={`hero ${className}`.trim()}>
      <h1 className="hero-title gradient-text">
        {title}
      </h1>
      
      {tagline && (
        <p className="hero-subtitle">
          {tagline}
        </p>
      )}
      
      {description && (
        <p className="hero-subtitle" style={{ fontSize: 'var(--font-size-lg)', marginTop: 'var(--space-lg)' }}>
          {description}
        </p>
      )}
      
      {cta && (
        <div style={{ marginTop: 'var(--space-xl)' }}>
          <Button
            href={cta.href}
            onClick={cta.onClick}
            variant={cta.variant || 'primary'}
            size="lg"
            LinkComponent={LinkComponent}
          >
            {cta.label}
          </Button>
        </div>
      )}
    </section>
  )
}

