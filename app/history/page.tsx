import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'History | KVSHVL',
  description: 'Complete archive documenting two decades of work—150+ projects, collaborations, and teaching roles from 2006 to present.',
}

export default async function HistoryPage() {
  const { content } = await getMarkdownContent('history.md')
  
  return (
    <main style={{ padding: '2rem 1rem', maxWidth: '900px', margin: '0 auto' }}>
      <article 
        className="history-content"
        dangerouslySetInnerHTML={{ __html: content }}
        style={{
          lineHeight: '1.6',
        }}
      />
    </main>
  )
}

