import type { Metadata } from 'next'
import Link from 'next/link'
import { Card } from '@kushalsamant/design-template'
import fs from 'fs'
import path from 'path'

export const metadata: Metadata = {
  title: 'Projects | KVSHVL',
  description: 'Portfolio of architectural and design projects by Kushal Samant. Explore 150+ projects spanning spatial design, open-source building systems, and creative work.',
}

export default function ProjectsPage() {
  const projectsDirectory = path.join(process.cwd(), 'content', 'projects')
  
  let projects: string[] = []
  if (fs.existsSync(projectsDirectory)) {
    const files = fs.readdirSync(projectsDirectory)
    projects = files
      .filter(file => file.endsWith('.md'))
      .map(file => file.replace(/\.md$/, ''))
      .sort()
  }

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
    ],
  }

  const formatProjectName = (slug: string) => {
    return slug
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase())
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
      <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
        <article className="fade-in">
          <section className="hero" aria-labelledby="projects-title">
            <h1 id="projects-title" className="hero-title">Projects</h1>
            <p className="hero-subtitle">
              Portfolio of architectural and design projects. Explore spatial design, open-source building systems, and creative work.
            </p>
          </section>

          <section className="section" aria-labelledby="projects-list-title">
            <h2 id="projects-list-title" className="section-title">All Projects</h2>
            
            <div className="grid grid-2">
              {projects.map((project) => (
                <Link
                  key={project}
                  href={`/projects/${project}`}
                  style={{ display: 'block', textDecoration: 'none', color: 'inherit', cursor: 'pointer' }}
                >
                  <Card
                    variant="elevated"
                    className="slide-up"
                  >
                    <div>
                      <h3 style={{ 
                        fontSize: 'var(--font-size-xl)', 
                        marginBottom: 'var(--space-sm)',
                      }}>
                        {formatProjectName(project)}
                      </h3>
                      <p style={{ 
                        fontSize: 'var(--font-size-sm)',
                        color: 'var(--color-text-muted)',
                        margin: 0,
                      }}>
                        View project →
                      </p>
                    </div>
                  </Card>
                </Link>
              ))}
            </div>
          </section>
        </article>
      </main>
    </>
  )
}

