import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@kushalsamant/design-template'
import { AuthProvider } from '@/lib/auth-provider'
import HeaderWrapper from '@/components/HeaderWrapper'
import FooterWrapper from '@/components/FooterWrapper'
import '@kushalsamant/design-template/styles/globals.css'
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
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: 'Kushal Dhananjay Samant',
    alternateName: 'KVSHVL',
    jobTitle: 'Licensed Architect & SaaS Developer',
    description: 'Licensed architect and software developer. Problem solver across architecture, SaaS development, and design. 150+ projects, 296 essays.',
    url: 'https://kvshvl.in',
    sameAs: [
      'https://www.linkedin.com/in/kvshvl',
      'https://github.com/kushalsamant',
      'https://www.instagram.com/kvshvl',
      'https://twitter.com/kvshvl_',
      'https://kvshvl.medium.com',
      'https://www.youtube.com/@kvshvl',
    ],
    email: 'writetokushaldsamant@gmail.com',
    telephone: '+91-87796-32310',
    address: {
      '@type': 'PostalAddress',
      streetAddress: 'H.No. 2337, "Visava", Swami Samarth Nagar, Near Dattanagar, Kavilgaon, Nerur',
      addressLocality: 'Kudal',
      postalCode: '416520',
      addressRegion: 'Maharashtra',
      addressCountry: 'IN',
    },
    knowsAbout: [
      'Architecture',
      'SaaS Development',
      'Web Design',
      'Building Information Modeling',
      'Open Source Software',
    ],
    alumniOf: {
      '@type': 'EducationalOrganization',
      name: 'Architectural Education',
    },
  }

  return (
    <html lang="en" className={inter.variable}>
      <head>
        <meta name="theme-color" content="#ffffff" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
      </head>
      <body className={inter.className}>
        <AuthProvider>
        <ThemeProvider>
          <a href="#main-content" className="skip-link">
            Skip to main content
          </a>
          <HeaderWrapper />
          <main id="main-content">{children}</main>
          <FooterWrapper />
        </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
