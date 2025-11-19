import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Privacy Policy | KVSHVL',
  description: 'Privacy policy for KVSHVL and Kushal Samant services. Learn how we collect, use, and protect your personal information and data.',
}

export default async function PrivacyPolicyPage() {
  const { content } = await getMarkdownContent('privacypolicy.md')
  
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

