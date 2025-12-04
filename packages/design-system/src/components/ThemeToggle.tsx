'use client'

import { useEffect, useState } from 'react'
import { getStoredTheme, setStoredTheme, getEffectiveTheme, applyTheme, type Theme } from '../lib/theme'

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>('system')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    setTheme(getStoredTheme())
    applyTheme(getEffectiveTheme())
  }, [])

  const toggleTheme = () => {
    const current = getStoredTheme()
    let next: Theme
    
    if (current === 'light') {
      next = 'dark'
    } else if (current === 'dark') {
      next = 'system'
    } else {
      next = 'light'
    }
    
    setTheme(next)
    setStoredTheme(next)
    
    if (next === 'system') {
      applyTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    } else {
      applyTheme(next)
    }
  }

  if (!mounted) {
    return (
      <button
        className="theme-toggle"
        aria-label="Toggle theme"
        type="button"
      >
        <span aria-hidden="true">Theme</span>
      </button>
    )
  }

  const getIcon = () => {
    // Show the action (next theme) instead of current theme
    const effective = getEffectiveTheme()
    if (effective === 'dark') {
      return 'Light' // Currently dark, button will switch to light
    }
    return 'Dark' // Currently light, button will switch to dark
  }

  const getLabel = () => {
    // Show the action (next theme) instead of current theme
    const effective = getEffectiveTheme()
    if (theme === 'system') {
      // In system mode, next is 'light', so show "Light"
      return 'Light'
    }
    // Show what the button will switch to
    if (effective === 'dark') {
      return 'Light' // Currently dark, button will switch to light (via system)
    }
    return 'Dark' // Currently light, button will switch to dark
  }

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label={`Toggle theme. Current: ${getLabel()}`}
      type="button"
      title={getLabel()}
    >
      <span aria-hidden="true">{getIcon()}</span>
    </button>
  )
}

