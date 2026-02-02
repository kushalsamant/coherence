import React, { type ReactNode } from 'react'

interface Stat {
  value: string | number
  label: string
  description?: string
}

interface StatsDisplayProps {
  stats: Stat[]
  className?: string
  columns?: 2 | 3 | 4
}

export default function StatsDisplay({
  stats,
  className = '',
  columns = 3,
}: StatsDisplayProps) {
  const gridClass = `grid grid-${columns}`
  
  return (
    <div className={`${gridClass} ${className}`.trim()} style={{ gap: 'var(--space-xl)' }}>
      {stats.map((stat, index) => (
        <div key={index} className="slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
          <div style={{ 
            fontSize: 'var(--font-size-4xl)', 
            fontWeight: 'var(--font-weight-bold)',
            marginBottom: 'var(--space-sm)',
          }}>
            {stat.value}
          </div>
          <div style={{ 
            fontSize: 'var(--font-size-lg)',
            color: 'var(--color-text-secondary)',
            marginBottom: stat.description ? 'var(--space-xs)' : 0,
          }}>
            {stat.label}
          </div>
          {stat.description && (
            <div style={{ 
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-muted)',
            }}>
              {stat.description}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

