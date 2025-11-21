'use client'

export type Theme = 'light' | 'dark' | 'system'

const THEME_STORAGE_KEY = 'kvshvl-theme'

export function getStoredTheme(): Theme {
  if (typeof window === 'undefined') return 'system'
  const stored = localStorage.getItem(THEME_STORAGE_KEY) as Theme | null
  return stored || 'system'
}

export function setStoredTheme(theme: Theme): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(THEME_STORAGE_KEY, theme)
}

export function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export function getEffectiveTheme(): 'light' | 'dark' {
  const theme = getStoredTheme()
  if (theme === 'system') {
    return getSystemTheme()
  }
  return theme
}

export function applyTheme(theme: 'light' | 'dark'): void {
  if (typeof document === 'undefined') return
  
  const root = document.documentElement
  root.setAttribute('data-theme', theme)
  
  // Update meta theme-color
  const metaThemeColor = document.querySelector('meta[name="theme-color"]')
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', theme === 'dark' ? '#0a0a0a' : '#ffffff')
  }
}

export function initTheme(): (() => void) | void {
  if (typeof window === 'undefined') return
  
  const effectiveTheme = getEffectiveTheme()
  applyTheme(effectiveTheme)
  
  // Listen for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const handleChange = () => {
    const stored = getStoredTheme()
    if (stored === 'system') {
      applyTheme(getSystemTheme())
    }
  }
  
  mediaQuery.addEventListener('change', handleChange)
  
  // Cleanup function (returned for use in useEffect)
  return () => {
    mediaQuery.removeEventListener('change', handleChange)
  }
}

