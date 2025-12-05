'use client'

export type Theme = 'light' | 'dark' | 'system'

const THEME_STORAGE_KEY = 'kvshvl-theme'

export function getStoredTheme(): Theme {
  // Always return 'light' - dark mode disabled
  return 'light'
}

export function setStoredTheme(theme: Theme): void {
  // No-op - theme switching disabled
  return
}

export function getSystemTheme(): 'light' | 'dark' {
  // Always return 'light' - dark mode disabled
  return 'light'
}

export function getEffectiveTheme(): 'light' | 'dark' {
  // Always return 'light' - dark mode disabled
  return 'light'
}

export function applyTheme(theme: 'light' | 'dark'): void {
  if (typeof document === 'undefined') return
  
  const root = document.documentElement
  
  // Force light theme - always set to 'light'
  root.setAttribute('data-theme', 'light')
  
  // Remove dark class - light mode only
    root.classList.remove('dark')
  
  // Update meta theme-color - always light
  const metaThemeColor = document.querySelector('meta[name="theme-color"]')
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', '#ffffff')
  }
}

export function initTheme(): (() => void) | void {
  if (typeof window === 'undefined') return
  
  // Always apply light theme
  applyTheme('light')
  
  // No need to listen for system theme changes - light mode only
  // Return empty cleanup function for compatibility
  return () => {}
}

