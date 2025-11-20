import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Terms of Service | KVSHVL',
  description: 'Terms of Service for KVSHVL products and Kushal Samant consulting services. Legal terms governing use of our services, intellectual property, and user obligations.',
}

export default async function TermsOfServicePage() {
  const { content } = await getMarkdownContent('docs/termsofservice.md')
  
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

