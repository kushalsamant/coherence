import React from 'react'
import Card from './Card'

interface NewsCardProps {
  title: string
  description?: string
  image?: string
  imageAlt?: string
  href?: string
  category?: string
  date?: string
  className?: string
  LinkComponent?: React.ComponentType<any>
}

export default function NewsCard({
  title,
  description,
  image,
  imageAlt,
  href,
  category,
  date,
  className = '',
  LinkComponent,
}: NewsCardProps) {
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
      
      <div style={{ marginBottom: 'var(--space-sm)' }}>
        {(category || date) && (
          <div style={{ 
            display: 'flex', 
            gap: 'var(--space-md)',
            marginBottom: 'var(--space-sm)',
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
          }}>
            {category && <span>{category}</span>}
            {date && <time>{date}</time>}
          </div>
        )}
        
        <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-sm)' }}>
          {title}
        </h3>
      </div>
      
      {description && (
        <p style={{ 
          color: 'var(--color-text-secondary)',
          marginBottom: 'var(--space-md)',
        }}>
          {description}
        </p>
      )}
      
      {href && (
        <div style={{ marginTop: 'var(--space-md)' }}>
          {LinkComponent ? (
            <LinkComponent href={href} className="inline-flex items-center gap-2">
              View more <span aria-hidden="true">→</span>
            </LinkComponent>
          ) : (
            <a
              href={href}
              style={{ display: 'inline-flex', alignItems: 'center', gap: 'var(--space-xs)' }}
            >
              View more <span aria-hidden="true">→</span>
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
