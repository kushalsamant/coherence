import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'History | KVSHVL',
  description: 'Complete archive documenting two decades of work—150+ projects, collaborations, and teaching roles from 2006 to present.',
}

export default async function HistoryPage() {
  const { content } = await getMarkdownContent('docs/history.md')
  
  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article 
        className="history-content"
        dangerouslySetInnerHTML={{ __html: content }}
      />
    </main>
  )
}

