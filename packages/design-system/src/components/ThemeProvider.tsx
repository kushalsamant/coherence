'use client'

import React, { useEffect } from 'react'
import { initTheme } from '../lib/theme'
import { initScrollAnimations } from '../lib/scroll-animations'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize light theme (forced)
    initTheme()
    const cleanup = initScrollAnimations()
    return cleanup
  }, [])

  return <>{children}</>
}
