import React, { type ReactNode } from 'react'
import Card from './Card'

interface ProjectCardProps {
  title: string
  description: string
  image?: string
  imageAlt?: string
  href?: string
  tags?: string[]
  date?: string
  className?: string
  LinkComponent?: React.ComponentType<any>
}

export default function ProjectCard({
  title,
  description,
  image,
  imageAlt,
  href,
  tags,
  date,
  className = '',
  LinkComponent,
}: ProjectCardProps) {
  const content = (
    <>
      {image && (
        <div style={{ marginBottom: 'var(--space-md)' }}>
          <img
            src={image}
            alt={imageAlt || title}
            style={{
              width: '100%',
              height: 'auto',
              borderRadius: 'var(--radius-lg)',
              objectFit: 'cover',
            }}
          />
        </div>
      )}
      
      <div style={{ marginBottom: 'var(--space-md)' }}>
        <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-sm)' }}>
          {title}
        </h3>
      </div>
      
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-lg)' }}>
        {description}
      </p>
      
      {(tags || date) && (
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: 'var(--space-sm)',
          marginTop: 'var(--space-md)',
        }}>
          {tags?.map((tag) => (
            <span
              key={tag}
              style={{
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-muted)',
                padding: 'var(--space-xs) var(--space-sm)',
                background: 'var(--color-background-secondary)',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              {tag}
            </span>
          ))}
          {date && (
            <span
              style={{
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-muted)',
              }}
            >
              {date}
            </span>
          )}
        </div>
      )}
      
      {href && (
        <div style={{ marginTop: 'var(--space-md)' }}>
          {LinkComponent ? (
            <LinkComponent href={href} className="inline-flex items-center gap-2">
              View <span aria-hidden="true">→</span>
            </LinkComponent>
          ) : (
            <a
              href={href}
              style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)' }}
            >
              View <span aria-hidden="true">→</span>
            </a>
          )}
        </div>
      )}
    </>
  )

  if (href && LinkComponent) {
    return (
      <Card variant="elevated" className={className}>
        <LinkComponent href={href} style={{ textDecoration: 'none', color: 'inherit' }}>
          {content}
        </LinkComponent>
      </Card>
    )
  }

  return (
    <Card variant="elevated" className={className}>
      {content}
    </Card>
  )
}

