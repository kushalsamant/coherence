import React from 'react'

interface Client {
  name: string
  logo?: string
  logoAlt?: string
  href?: string
}

interface ClientGridProps {
  clients: Client[]
  className?: string
  columns?: 3 | 4 | 5 | 6
  LinkComponent?: React.ComponentType<any>
}

export default function ClientGrid({
  clients,
  className = '',
  columns = 4,
  LinkComponent,
}: ClientGridProps) {
  const gridClass = `grid grid-${columns}`
  
  return (
    <div className={`${gridClass} ${className}`.trim()} style={{ gap: 'var(--space-xl)' }}>
      {clients.map((client, index) => {
        const content = client.logo ? (
          <img
            src={client.logo}
            alt={client.logoAlt || client.name}
            style={{
              width: '100%',
              height: 'auto',
              maxHeight: '60px',
              objectFit: 'contain',
              filter: 'opacity(0.7)',
              transition: 'filter var(--transition-fast)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.filter = 'opacity(1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.filter = 'opacity(0.7)'
            }}
          />
        ) : (
          <span style={{ color: 'var(--color-text-secondary)' }}>{client.name}</span>
        )

        if (client.href) {
          if (LinkComponent) {
            return (
              <LinkComponent
                key={index}
                href={client.href}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  textDecoration: 'none',
                }}
              >
                {content}
              </LinkComponent>
            )
          }
          
          return (
            <a
              key={index}
              href={client.href}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                textDecoration: 'none',
              }}
            >
              {content}
            </a>
          )
        }

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {content}
          </div>
        )
      })}
    </div>
  )
}
