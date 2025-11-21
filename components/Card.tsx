import { type ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  variant?: 'default' | 'elevated' | 'outlined'
  className?: string
  hover?: boolean
  onClick?: () => void
}

export default function Card({
  children,
  variant = 'default',
  className = '',
  hover = true,
  onClick,
}: CardProps) {
  const baseClasses = 'card'
  const variantClasses = variant === 'elevated' ? 'card-elevated' : variant === 'outlined' ? 'card-outlined' : ''
  const hoverClass = hover ? 'card-hover' : ''
  const classes = `${baseClasses} ${variantClasses} ${hoverClass} ${className}`.trim()

  if (onClick) {
    return (
      <div
        className={classes}
        onClick={onClick}
        role="button"
        tabIndex={0}
        aria-label={typeof children === 'string' ? children : 'Interactive card'}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            onClick()
          }
        }}
      >
        {children}
      </div>
    )
  }

  return (
    <div className={classes}>
      {children}
    </div>
  )
}

