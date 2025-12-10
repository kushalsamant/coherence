'use client'

import React, { useEffect } from 'react'
import { initScrollAnimations } from '../lib/scroll-animations'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Ensure light theme (no dark mode)
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', 'light')
      document.documentElement.classList.remove('dark')
    }
    
    const cleanup = initScrollAnimations()
    return cleanup
  }, [])

  return <>{children}</>
}
