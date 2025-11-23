import { getMarkdownContent } from '@/lib/process-markdown'
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import fs from 'fs'
import path from 'path'

export async function generateStaticParams() {
  const projectsDirectory = path.join(process.cwd(), 'projects')
  
  if (!fs.existsSync(projectsDirectory)) {
    return []
  }

  const files = fs.readdirSync(projectsDirectory)
  const markdownFiles = files.filter(file => file.endsWith('.md'))
  
  return markdownFiles.map((file) => ({
    slug: file.replace(/\.md$/, ''),
  }))
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const projectPath = path.join(process.cwd(), 'projects', `${params.slug}.md`)
  
  if (!fs.existsSync(projectPath)) {
    return {
      title: 'Project Not Found | KVSHVL',
    }
  }

  try {
    const { frontmatter } = await getMarkdownContent(`projects/${params.slug}.md`)
    const title = frontmatter.title || `${params.slug.replace(/_/g, ' ')} | KVSHVL`
    
    return {
      title,
      description: frontmatter.description || `Project: ${params.slug.replace(/_/g, ' ')}`,
    }
  } catch {
    return {
      title: `${params.slug.replace(/_/g, ' ')} | KVSHVL`,
    }
  }
}

export default async function ProjectPage({ params }: { params: { slug: string } }) {
  const projectPath = path.join(process.cwd(), 'projects', `${params.slug}.md`)
  
  if (!fs.existsSync(projectPath)) {
    notFound()
  }

  try {
    const { content } = await getMarkdownContent(`projects/${params.slug}.md`)
    
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
          name: 'Projects',
          item: 'https://kvshvl.in/projects',
        },
        {
          '@type': 'ListItem',
          position: 3,
          name: params.slug.replace(/_/g, ' '),
          item: `https://kvshvl.in/projects/${params.slug}`,
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
            className="project-content"
            dangerouslySetInnerHTML={{ __html: content }}
          />
        </main>
      </>
    )
  } catch (error) {
    notFound()
  }
}

