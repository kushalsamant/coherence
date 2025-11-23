import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'History | KVSHVL',
  description: 'Complete archive documenting two decades of work—150+ projects, collaborations, and teaching roles from 2006 to present.',
}

export default async function HistoryPage() {
  const { content } = await getMarkdownContent('docs/history.md')
  
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://kvshvl.in',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'History',
        item: 'https://kvshvl.in/history',
      },
    ],
  }
  
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article 
        className="history-content"
        dangerouslySetInnerHTML={{ __html: content }}
      />
    </main>
    </>
  )
}

