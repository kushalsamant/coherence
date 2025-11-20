import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import AppHeader from '@/components/AppHeader'
import AppFooter from '@/components/AppFooter'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: {
    default: 'KVSHVL',
    template: '%s | KVSHVL',
  },
  description: 'Licensed architect and software developer. Problem solver across architecture, SaaS development, and design. 150+ projects, 296 essays.',
  keywords: 'Architecture, CSS, HTML, Javascript, People, Places, Visual Art, Web',
  authors: [{ name: 'Kushal Samant' }],
  creator: 'Kushal Samant',
  publisher: 'Kushal Samant',
  openGraph: {
    title: 'KVSHVL',
    description: 'Licensed architect and software developer. Problem solver across architecture, SaaS development, and design.',
    url: 'https://kvshvl.in',
    siteName: 'KVSHVL',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'KVSHVL',
    description: 'Licensed architect and software developer. Problem solver across architecture, SaaS development, and design.',
    site: '@kvshvl_',
    creator: '@kvshvl_',
  },
  metadataBase: new URL('https://kvshvl.in'),
  robots: {
    index: true,
    follow: true,
  },
}

export const viewport: Viewport = {
  themeColor: '#9333EA',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={inter.className}>
        <AppHeader />
        <main>{children}</main>
        <AppFooter />
      </body>
    </html>
  )
}
