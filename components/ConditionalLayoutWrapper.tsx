'use client'

import { usePathname } from 'next/navigation'
import { Suspense } from 'react'
import HeaderWrapper from '@/components/HeaderWrapper'
import FooterWrapper from '@/components/FooterWrapper'

function LayoutContent({ children }: { children: React.ReactNode }) {
  // Render all routes with header and footer
  return (
    <>
      <HeaderWrapper />
      <main>{children}</main>
      <FooterWrapper />
    </>
  )
}

export default function ConditionalLayoutWrapper({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <Suspense fallback={<main>{children}</main>}>
      <LayoutContent>{children}</LayoutContent>
    </Suspense>
  )
}
