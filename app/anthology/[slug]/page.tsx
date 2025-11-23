import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import fs from 'fs'
import path from 'path'

export async function generateStaticParams() {
  const anthologyDirectory = path.join(process.cwd(), 'anthology')
  
  if (!fs.existsSync(anthologyDirectory)) {
    return []
  }

  const files = fs.readdirSync(anthologyDirectory)
  const markdownFiles = files.filter(file => file.endsWith('.md'))
  
  return markdownFiles.map((file) => ({
    slug: file.replace(/\.md$/, ''),
  }))
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const anthologyPath = path.join(process.cwd(), 'anthology', `${params.slug}.md`)
  
  if (!fs.existsSync(anthologyPath)) {
    return {
      title: 'Post Not Found | KVSHVL',
    }
  }

  try {
    const { frontmatter } = await getMarkdownContent(`anthology/${params.slug}.md`)
    const title = frontmatter.title || `${params.slug.replace(/_/g, ' ')} | KVSHVL`
    
    return {
      title,
      description: frontmatter.description || `Anthology post: ${params.slug.replace(/_/g, ' ')}`,
    }
  } catch {
    return {
      title: `${params.slug.replace(/_/g, ' ')} | KVSHVL`,
    }
  }
}

export default async function AnthologyPage({ params }: { params: { slug: string } }) {
  const anthologyPath = path.join(process.cwd(), 'anthology', `${params.slug}.md`)
  
  if (!fs.existsSync(anthologyPath)) {
    notFound()
  }

  try {
    const { content } = await getMarkdownContent(`anthology/${params.slug}.md`)
    
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
          name: 'Anthology',
          item: 'https://kvshvl.in/anthology',
        },
        {
          '@type': 'ListItem',
          position: 3,
          name: params.slug.replace(/_/g, ' '),
          item: `https://kvshvl.in/anthology/${params.slug}`,
        },
      ],
    }

    const articleSchema = {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: params.slug.replace(/_/g, ' '),
      url: `https://kvshvl.in/anthology/${params.slug}`,
    }

    return (
      <>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
        />
        <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
          <article 
            className="anthology-content"
            dangerouslySetInnerHTML={{ __html: content }}
          />
        </main>
      </>
    )
  } catch (error) {
    notFound()
  }
}

