'use client'

import { useEffect } from 'react'
import { initTheme } from '@/lib/theme'
import { initScrollAnimations } from '@/lib/scroll-animations'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    initTheme()
    const cleanup = initScrollAnimations()
    return cleanup
  }, [])

  return <>{children}</>
}

