import React, { type ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  variant?: 'default' | 'elevated' | 'outlined'
  className?: string
  hover?: boolean
  onClick?: () => void
  href?: string
  LinkComponent?: React.ComponentType<any>
  style?: React.CSSProperties
}

export default function Card({
  children,
  variant = 'default',
  className = '',
  hover = true,
  onClick,
  href,
  LinkComponent,
  style,
}: CardProps) {
  const baseClasses = 'card'
  const variantClasses = variant === 'elevated' ? 'card-elevated' : variant === 'outlined' ? 'card-outlined' : ''
  const hoverClass = hover ? 'card-hover' : ''
  const classes = `${baseClasses} ${variantClasses} ${hoverClass} ${className}`.trim()

  // If href is provided, render as link
  if (href) {
    const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
      <a href={href} className={className} {...props}>{children}</a>
    ))
    
    return (
      <Link
        href={href}
        className={classes}
        style={{ ...style, textDecoration: 'none', color: 'inherit', display: 'block' }}
      >
        {children}
      </Link>
    )
  }

  if (onClick) {
    return (
      <div
        className={classes}
        style={style}
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
    <div className={classes} style={style}>
      {children}
    </div>
  )
}

