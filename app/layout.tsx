import type { Metadata, Viewport } from 'next'
import { headers } from 'next/headers'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@kushalsamant/design-template'
import { AuthProvider } from '@/lib/auth-provider'
import { getCurrentSession } from '@/lib/auth'
import ConditionalLayoutWrapper from '@/components/ConditionalLayoutWrapper'
import Analytics from '@/components/Analytics'
import '@kushalsamant/design-template/styles/globals.css'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: {
    default: 'Sketch2BIM - Transform Sketches into BIM Models',
    template: '%s | Sketch2BIM',
  },
  description: 'Transform hand-drawn architectural sketches into BIM models. Building information modeling for architectural, landscape, urban design, and urban planning projects. Convert your sketches into industry-standard IFC, DWG, RVT, and SKP formats.',
  keywords: 'BIM, Building Information Modeling, Architecture, Sketch to BIM, IFC, CAD, Architectural Design, Sketch Conversion',
  authors: [{ name: 'Kushal Samant' }],
  creator: 'Kushal Samant',
  publisher: 'Kushal Samant',
  openGraph: {
    title: 'Sketch2BIM - Transform Sketches into BIM Models',
    description: 'Transform hand-drawn architectural sketches into BIM models. Building information modeling for architectural, landscape, urban design, and urban planning projects. Convert your sketches into industry-standard IFC, DWG, RVT, and SKP formats.',
    url: 'https://kvshvl.in',
    siteName: 'Sketch2BIM',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Sketch2BIM - Transform Sketches into BIM Models',
    description: 'Transform hand-drawn architectural sketches into BIM models. Building information modeling for architectural, landscape, urban design, and urban planning projects. Convert your sketches into industry-standard IFC, DWG, RVT, and SKP formats.',
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

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getCurrentSession();
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
    <html lang="en" className={inter.variable} data-theme="light">
      <head>
        <meta name="theme-color" content="#ffffff" />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Ensure light theme (no dark mode)
              document.documentElement.setAttribute('data-theme', 'light');
              document.documentElement.classList.remove('dark');
            `,
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
        {/* Google Analytics */}
        {process.env.NEXT_PUBLIC_GA_ID && (
          <>
            <script
              async
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
            />
            <script
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}', {
                    page_path: window.location.pathname,
                  });
                `,
              }}
            />
          </>
        )}
        {/* Plausible Analytics */}
        {process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN && (
          <script
            defer
            data-domain={process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN}
            src="https://plausible.io/js/script.js"
          />
        )}
      </head>
      <body className={inter.className}>
        <AuthProvider>
        <ThemeProvider>
          <Analytics />
          <ConditionalLayoutWrapper>
            {children}
          </ConditionalLayoutWrapper>
        </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
