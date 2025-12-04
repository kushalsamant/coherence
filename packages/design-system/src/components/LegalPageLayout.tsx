import React from 'react'
import type { ReactNode } from 'react'

interface LegalPageLayoutProps {
  title: string
  children: ReactNode
  appName?: string
  homeLink?: string
  lastUpdated?: Date
  className?: string
  LinkComponent?: React.ComponentType<any>
  FooterComponent?: React.ComponentType<any>
}

export default function LegalPageLayout({
  title,
  children,
  appName = 'App',
  homeLink = '/',
  lastUpdated,
  className = '',
  LinkComponent,
  FooterComponent,
}: LegalPageLayoutProps) {
  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <div className={`min-h-screen bg-gray-50 ${className}`.trim()}>
      {/* Header */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href={homeLink} className="text-2xl font-bold text-primary-600">
              {appName}
            </Link>
            <Link href={homeLink} className="text-gray-700 hover:text-primary-600">
              Back to Home
            </Link>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">{title}</h1>
        <div className="prose prose-lg max-w-none">
          {lastUpdated && (
            <p className="text-gray-600 mb-4">
              Last updated: {lastUpdated.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          )}
          {children}
        </div>
      </div>

      {/* Footer */}
      {FooterComponent && <FooterComponent />}
    </div>
  )
}

