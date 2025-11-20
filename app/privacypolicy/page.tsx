import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Privacy Policy | KVSHVL',
  description: 'Privacy policy for KVSHVL and Kushal Samant services. Learn how we collect, use, and protect your personal information and data.',
}

export default async function PrivacyPolicyPage() {
  const { content } = await getMarkdownContent('docs/privacypolicy.md')
  
  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article 
        className="legal-content"
        dangerouslySetInnerHTML={{ __html: content }}
      />
    </main>
  )
}

