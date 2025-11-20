import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Cancellation & Refund Policy | KVSHVL',
  description: 'Cancellation & Refund Policy for KVSHVL products and Kushal Samant consulting services. Detailed terms for cancelling subscriptions, refund eligibility, and processing timelines.',
}

export default async function CancellationRefundPage() {
  const { content } = await getMarkdownContent('docs/cancellationrefund.md')
  
  return (
    <main style={{ padding: '2rem 1rem', maxWidth: '900px', margin: '0 auto' }}>
      <article 
        className="legal-content"
        dangerouslySetInnerHTML={{ __html: content }}
        style={{
          lineHeight: '1.6',
        }}
      />
    </main>
  )
}

