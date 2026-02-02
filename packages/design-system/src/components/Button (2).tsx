import React, { type ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  href?: string
  onClick?: () => void
  disabled?: boolean
  className?: string
  type?: 'button' | 'submit' | 'reset'
  target?: string
  rel?: string
  LinkComponent?: React.ComponentType<any>
  style?: React.CSSProperties
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  href,
  onClick,
  disabled = false,
  className = '',
  type = 'button',
  target,
  rel,
  LinkComponent,
  style,
}: ButtonProps) {
  const baseClasses = 'btn'
  const variantClasses = `btn-${variant}`
  const sizeClasses = size === 'sm' ? 'btn-sm' : size === 'lg' ? 'btn-lg' : ''
  const classes = `${baseClasses} ${variantClasses} ${sizeClasses} ${className}`.trim()

  if (href) {
    if (LinkComponent) {
      return (
        <LinkComponent
          href={href}
          className={classes}
          style={style}
          target={target}
          rel={rel}
          onClick={onClick}
        >
          {children}
        </LinkComponent>
      )
    }
    
    return (
      <a
        href={href}
        className={classes}
        style={style}
        target={target}
        rel={rel}
        onClick={onClick}
        aria-disabled={disabled}
      >
        {children}
      </a>
    )
  }

  return (
    <button
      type={type}
      className={classes}
      style={style}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

